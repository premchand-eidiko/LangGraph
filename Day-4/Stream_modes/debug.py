from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    message: str


def greeting_node(state: State):
    return {
        "message": f"Hello {state['name']}"
    }


graph = StateGraph(State)

graph.add_node("greeting", greeting_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", END)

app = graph.compile()


input_data = {
    "name": "Prem",
    "message": ""
}


for chunk in app.stream(
    input_data,
    stream_mode="debug"
):
    print(chunk)