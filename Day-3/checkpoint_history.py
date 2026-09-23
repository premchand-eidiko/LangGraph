from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    step1: str
    step2: str
    step3: str
    step4: str
    step5: str


def node1(state: State):
    state["step1"] = "completed"
    return state


def node2(state: State):
    state["step2"] = "completed"
    return state


def node3(state: State):
    state["step3"] = "completed"
    return state


def node4(state: State):
    state["step4"] = "completed"
    return state


def node5(state: State):
    state["step5"] = "completed"
    return state


graph = StateGraph(State)

graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)
graph.add_node("node4", node4)
graph.add_node("node5", node5)

graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", "node3")
graph.add_edge("node3", "node4")
graph.add_edge("node4", "node5")
graph.add_edge("node5", END)

memory = MemorySaver()

app = graph.compile(checkpointer=memory)

config = {
    "configurable": {
        "thread_id": "test-1"
    }
}

initial_state = {
    "step1": "",
    "step2": "",
    "step3": "",
    "step4": "",
    "step5": ""
}

result = app.invoke(initial_state, config)

print("\nCURRENT STATE")
print(result)

print("\nCHECKPOINT HISTORY")

history = list(app.get_state_history(config))

for i, checkpoint in enumerate(history):
    print(f"\nCheckpoint {i + 1}")
    print(checkpoint.values)
    print("Checkpoint ID:", checkpoint.config["configurable"]["checkpoint_id"])