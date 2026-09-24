from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    task1_result: str
    task2_result: str
    task3_result: str
    final_result: str

def task1(state: State):
    print("Task 1 executing...")
    return { "task1_result": "Result from Task 1" }

def task2(state: State):
    print("Task 2 executing...")
    return { "task2_result": "Result from Task 2" }

def task3(state: State):
    print("Task 3 executing...")
    return { "task3_result": "Result from Task 3" }

def combine_results(state: State):
    print("Combining results...")
    combined = (
        f"{state['task1_result']}\n"
        f"{state['task2_result']}\n"
        f"{state['task3_result']}"
    )
    return { "final_result": combined }

graph = StateGraph(State)

graph.add_node("task1", task1)
graph.add_node("task2", task2)
graph.add_node("task3", task3)
graph.add_node("combine_results", combine_results)

graph.add_edge(START, "task1")
graph.add_edge(START, "task2")
graph.add_edge(START, "task3")

graph.add_edge("task1", "combine_results")
graph.add_edge("task2", "combine_results")
graph.add_edge("task3", "combine_results")

graph.add_edge("combine_results", END)

app = graph.compile()

input_data = {
    "task1_result": "",
    "task2_result": "",
    "task3_result": "",
    "final_result": ""
}

result = app.invoke(input_data)

print("\nFinal Result:")
print(result["final_result"])