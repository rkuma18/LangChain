import json
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()
tavily_tool = TavilySearchResults(max_results=5)

def execute_tools(state: dict) -> dict:
    messages = state["messages"]
    last_ai_message: AIMessage = messages[-1]

    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        return {"messages": messages}

    tool_messages = []

    for tool_call in last_ai_message.tool_calls:
        if tool_call['name'] in ['AnswerQuestion', 'ReviseAnswer']:
            call_id = tool_call['id']
            search_queries = tool_call['args'].get('search_queries', [])

            query_result = {}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                query_result[query] = result

            tool_messages.append(
                ToolMessage(
                    tool_call_id=call_id,
                    content=json.dumps(query_result, indent=2)
                )
            )

    return {"messages": messages + tool_messages}
