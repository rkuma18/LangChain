from langgraph.graph import StateGraph, END
from langgraph.types import Command
from typing import TypedDict
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

class State(TypedDict):
    value: str

# Node A
def node_a(state: State): 
    print("Node A")
    return Command(
        goto="node_b",
        update={"value": state["value"] + "a"}
    )

# Node B - handles user input inline
def node_b(state: State): 
    print("Node B")
    user_input = input("Do you want to go to C or D? Type C/D: ").strip().upper()
    while user_input not in ("C", "D"):
        user_input = input("Invalid input. Please type C or D: ").strip().upper()

    next_node = "node_c" if user_input == "C" else "node_d"

    return Command(
        goto=next_node,
        update={"value": state["value"] + "b"}
    )

# Node C
def node_c(state: State): 
    print("Node C")
    return Command(
        goto=END,
        update={"value": state["value"] + "c"}
    )

# Node D
def node_d(state: State): 
    print("Node D")
    return Command(
        goto=END,
        update={"value": state["value"] + "d"}
    )

# Build the graph
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)
graph.add_node("node_d", node_d)

graph.set_entry_point("node_a")
graph.add_edge("node_c", END)
graph.add_edge("node_d", END)

# Compile and run
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
initial_state = {"value": ""}

result = app.invoke(initial_state, config)
print("\n✅ Final State:", result)

