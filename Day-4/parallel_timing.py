from typing import TypedDict
import time

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    task1: str
    task2: str
    task3: str

def task1(state: State):
    print(f"\nStarted at: {start_time:.2f} seconds")
    print("Task 1 started...")
    time.sleep(2)
    print("Task 1 completed...")
    return { "task1": "Task 1 completed" }

def task2(state: State):
    print(f"\nStarted at: {start_time:.2f} seconds")
    print("Task 2 started...")
    time.sleep(2)
    print("Task 2 completed...")
    return { "task2": "Task 2 completed" }

def task3(state: State):
    print(f"\nStarted at: {start_time:.2f} seconds")
    print("Task 3 started...")
    time.sleep(2)
    print("Task 3 completed...")
    return { "task3": "Task 3 completed" }

graph = StateGraph(State)

graph.add_node("task1", task1)
graph.add_node("task2", task2)
graph.add_node("task3", task3)

graph.add_edge(START, "task1")
graph.add_edge(START, "task2")
graph.add_edge(START, "task3")

graph.add_edge("task1", END)
graph.add_edge("task2", END)
graph.add_edge("task3", END)

app = graph.compile()

input_data = {
    "task1": "",
    "task2": "",
    "task3": ""
}

start_time = time.time()

result = app.invoke(input_data)

end_time = time.time()

print("\nFinal Result:")
print(result)

print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")