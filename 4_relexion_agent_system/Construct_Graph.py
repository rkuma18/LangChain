from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from Initial_responder import first_responder, revisor
from execute_tools import execute_tools

class State(TypedDict):
    messages: Annotated[list, add_messages]

MAX_ITERATIONS = 5
builder = StateGraph(State)
builder.add_node("draft", first_responder.respond)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor.respond)

builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")


def _get_num_iterations(messages: list):
    i = 0
    for m in messages[::-1]:
        if m.type not in {"tool", "ai"}:
            break
        i += 1
    return i

def event_loop(state: dict):
    num_iterations = _get_num_iterations(state["messages"])
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
builder.add_edge(START, "draft")
graph = builder.compile()

from langchain_core.messages import HumanMessage

events = graph.stream({"messages": [HumanMessage(content="After Repo rate cut by RBI, which Indian stock to perform well in coming months")]}, stream_mode="values")

for i, step in enumerate(events):
    print(f"\nStep {i}")
    step["messages"][-1].pretty_print()
