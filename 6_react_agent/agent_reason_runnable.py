from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_react_agent, tool
from langchain_community.tools import TavilySearchResults
import datetime
from langchain import hub
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Returns the current system time formatted using the provided strftime format string.
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool,get_system_time]
react_prompt= hub.pull("hwchase17/react")

react_agent_runnable = create_react_agent(
    tools=tools, 
    llm=llm,
    prompt=react_prompt
    )

