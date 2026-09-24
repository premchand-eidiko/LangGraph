from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer


class State(TypedDict):
    name: str
    message: str


def greeting_node(state: State):

    writer = get_stream_writer()

    writer("Starting greeting...\n")

    message = f"Hello {state['name']}"

    writer("Greeting created...\n")

    return {
        "message": message
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
    stream_mode="custom"
):
    print(chunk)