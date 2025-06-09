from typing import List
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain

load_dotenv()

# Node names
GENERATE = "generate"
REFLECT = "reflect"

# Create graph
graph = MessageGraph()

# Node: Generate
def generate_node(state: List[BaseMessage]) -> List[BaseMessage]:
    response = generation_chain.invoke({"messages": state})
    return [HumanMessage(content=response.content)]

# Node: Reflect
def reflect_node(state: List[BaseMessage]) -> List[BaseMessage]:
    response = reflection_chain.invoke({"messages": state})
    return [HumanMessage(content=response.content)]

# Condition logic
def should_continue(state: List[BaseMessage]) -> str:
    return END if len(state) > 4 else REFLECT

# Build the graph
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)

graph.set_entry_point(GENERATE)

# explicitly define both outcomes in the mapping
graph.add_conditional_edges(GENERATE, should_continue, {
    REFLECT: REFLECT,
    END: END
})

graph.add_edge(REFLECT, GENERATE)

# Compile
app = graph.compile()

# Visualize
#print("\n--- Mermaid Graph ---")
#print(app.get_graph().draw_mermaid())

#print("\n--- ASCII Graph ---")
#app.get_graph().print_ascii()

# Run the graph
initial_input = [HumanMessage(content="AI agent will take over junior level software jobs")]
result = app.invoke(initial_input)

# Show final output
print("\n=== Final Result ===")
for message in result:
    print(f"{message.type}: {message.content}")
