from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# --------------------------------
# 1. Define the State
# --------------------------------

class State(TypedDict):
    name: str
    greeting: str
    final_response: str


# --------------------------------
# 2. Define Node 1
# --------------------------------

def greeting_node(state: State):
    name = state["name"]

    greeting = f"Hello {name}!"

    return {
        "greeting": greeting
    }


# --------------------------------
# 3. Define Node 2
# --------------------------------

def welcome_node(state: State):
    greeting = state["greeting"]

    final_response = (
        f"{greeting} "
        "Welcome to your first LangGraph workflow!"
    )

    return {
        "final_response": final_response
    }


# --------------------------------
# 4. Create the Graph
# --------------------------------

graph = StateGraph(State)


# --------------------------------
# 5. Add Nodes
# --------------------------------

graph.add_node("greeting_node", greeting_node)
graph.add_node("welcome_node", welcome_node)


# --------------------------------
# 6. Add Edges
# --------------------------------

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", "welcome_node")
graph.add_edge("welcome_node", END)


# --------------------------------
# 7. Compile the Graph
# --------------------------------

app = graph.compile()


# --------------------------------
# 8. Get User Input
# --------------------------------

name = input("Enter your name: ")


# --------------------------------
# 9. Run the Graph
# --------------------------------

result = app.invoke({
    "name": name,
    "greeting": "",
    "final_response": ""
})


# --------------------------------
# 10. Display the Result
# --------------------------------

print("\nFinal Output:")
print(result["final_response"])