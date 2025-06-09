from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import datetime

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(description="1-3 search queries to improve the answer.")

class ReviseAnswer(AnswerQuestion):
    references: list[str] = Field(description="Citations motivating your updated answer.")

class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    def respond(self, state: dict):
        response = []
        for attempt in range(3):
            response = self.runnable.invoke({"messages": state["messages"]})
            try:
                self.validator.invoke(response)
                return {"messages": state["messages"] + [response]}
            except ValidationError as e:
                state["messages"].append(
                    ToolMessage(
                        content=f"{repr(e)}\n\nPay close attention to the function schema.\n\n"
                        + self.validator.schema_json()
                        + " Respond by fixing all validation errors.",
                        tool_call_id=response.tool_calls[0]["id"],
                    )
                )
        return {"messages": state["messages"] + [response]}

actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     """
     You are expert researcher.\n
     Current time: {time}\n\n
     1. {first_instruction}\n
     2. Reflect and critique your answer. Be severe to maximize improvement.\n
     3. Recommend search queries to research information and improve your answer.
     """
     ),
    MessagesPlaceholder(variable_name="messages"),
    ("user", "Respond using the {function_name} function."),
]).partial(time=lambda: datetime.datetime.now().isoformat())

initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
) | llm.bind_tools(tools=[AnswerQuestion])

validator = PydanticToolsParser(tools=[AnswerQuestion])
first_responder = ResponderWithRetries(initial_answer_chain, validator)

revise_instructions = """
Revise your previous answer using the new information.\n
- Use previous critique to add or remove content.\n
- Add numerical citations.\n
- Add 'References' section below (not counted in 250 words)."""

revision_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])

revision_validator = PydanticToolsParser(tools=[ReviseAnswer])
revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)