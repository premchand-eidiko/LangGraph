from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    age: int
    city: str

def get_name(state: State):
    print("get_name executing...")
    return { "name": "Prem" }

def get_age(state: State):
    print("get_age executing...")
    return { "age": 25 }

def get_city(state: State):
    print("get_city executing...")
    return { "city": "Hyderabad" }

graph = StateGraph(State)

graph.add_node("get_name", get_name)
graph.add_node("get_age", get_age)
graph.add_node("get_city", get_city)

graph.add_edge(START, "get_name")
graph.add_edge(START, "get_age")
graph.add_edge(START, "get_city")

graph.add_edge("get_name", END)
graph.add_edge("get_age", END)
graph.add_edge("get_city", END)

app = graph.compile()

input_data = {
    "name": "",
    "age": 0,
    "city": ""
}

result = app.invoke(input_data)

print("\nFinal Result:")
print(result)