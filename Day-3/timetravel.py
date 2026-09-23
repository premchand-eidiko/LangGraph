from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# ============================================================
# 1. DEFINE THE GRAPH STATE
# ============================================================
# This state will be updated as each node executes.

class State(TypedDict):
    step1: str
    step2: str
    step3: str
    step4: str
    step5: str


# ============================================================
# 2. DEFINE THE NODES
# ============================================================
# Each node updates one part of the state.


def node1(state: State):
    print("Executing Node 1")

    state["step1"] = "completed"

    return state


def node2(state: State):
    print("Executing Node 2")

    state["step2"] = "completed"

    return state


def node3(state: State):
    print("Executing Node 3")

    state["step3"] = "completed"

    return state


def node4(state: State):
    print("Executing Node 4")

    state["step4"] = "completed"

    return state


def node5(state: State):
    print("Executing Node 5")

    state["step5"] = "completed"

    return state


# ============================================================
# 3. CREATE THE GRAPH
# ============================================================

graph = StateGraph(State)


# Add the nodes to the graph

graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)
graph.add_node("node4", node4)
graph.add_node("node5", node5)


# Define the execution flow

graph.add_edge(START, "node1")

graph.add_edge("node1", "node2")

graph.add_edge("node2", "node3")

graph.add_edge("node3", "node4")

graph.add_edge("node4", "node5")

graph.add_edge("node5", END)


# ============================================================
# 4. CREATE THE CHECKPOINTER
# ============================================================
# MemorySaver stores checkpoints in RAM.
#
# Because we are using a checkpointer, LangGraph will create
# state snapshots during graph execution.

memory = MemorySaver()


# Compile the graph with the checkpointer

app = graph.compile(
    checkpointer=memory
)


# ============================================================
# 5. CREATE A THREAD
# ============================================================
# thread_id identifies this particular workflow execution.
#
# All checkpoints created during this execution belong to
# this thread.

config = {
    "configurable": {
        "thread_id": "test-1"
    }
}


# ============================================================
# 6. INITIAL STATE
# ============================================================
# Initially, none of the five steps are completed.

initial_state = {
    "step1": "",
    "step2": "",
    "step3": "",
    "step4": "",
    "step5": ""
}


# ============================================================
# 7. FIRST EXECUTION
# ============================================================
# LangGraph executes:
#
# Node 1
#    ↓
# Node 2
#    ↓
# Node 3
#    ↓
# Node 4
#    ↓
# Node 5
#
# Checkpoints are created during this execution.

print("\n========== FIRST EXECUTION ==========\n")

result = app.invoke(
    initial_state,
    config
)


# Print the final state

print("\nFinal state:")
print(result)


# ============================================================
# 8. GET CHECKPOINT HISTORY
# ============================================================
# get_state_history() gives us the saved state snapshots
# belonging to this thread.
#
# We convert the result into a list so that we can access
# individual checkpoints using an index.

print("\n========== CHECKPOINT HISTORY ==========\n")

history = list(
    app.get_state_history(config)
)


# Print every checkpoint

for index, checkpoint in enumerate(history):

    print(f"Checkpoint {index}")

    # State stored in this checkpoint
    print("State:")
    print(checkpoint.values)

    # Metadata tells us information about the execution
    print("Step:")
    print(checkpoint.metadata.get("step"))

    # 'next' tells us which node(s) are next from this snapshot
    print("Next:")
    print(checkpoint.next)

    # Every checkpoint has its own checkpoint ID
    print("Checkpoint ID:")
    print(
        checkpoint.config["configurable"]["checkpoint_id"]
    )

    print("----------------------------------------")


# ============================================================
# 9. SELECT AN OLD CHECKPOINT
# ============================================================
# Here we select one checkpoint from the history.
#
# IMPORTANT:
# history[2] means the third item in the Python list.
#
# The exact state represented depends on the checkpoint
# ordering returned by LangGraph.

print("\n========== SELECT A CHECKPOINT ==========\n")

selected_checkpoint = history[2]


# Get the ID of the selected checkpoint

checkpoint_id = (
    selected_checkpoint
    .config["configurable"]["checkpoint_id"]
)


print("Selected checkpoint ID:")
print(checkpoint_id)


# Print the state stored in that checkpoint

print("\nSelected checkpoint state:")
print(selected_checkpoint.values)


# ============================================================
# 10. CREATE CONFIG FOR THE OLD CHECKPOINT
# ============================================================
# Normally our config only contains:
#
# thread_id
#
# Now we also provide:
#
# checkpoint_id
#
# This tells LangGraph:
#
# "For this thread, I specifically want this checkpoint."

old_config = {
    "configurable": {
        "thread_id": "test-1",

        "checkpoint_id": checkpoint_id
    }
}


# ============================================================
# 11. RECOVER / READ THE OLD STATE
# ============================================================
# get_state() with old_config retrieves the state associated
# with the selected historical checkpoint.
#
# This does NOT execute the graph again.
#
# It simply reads the old checkpoint.

print("\n========== RECOVER OLD STATE ==========\n")

old_state = app.get_state(
    old_config
)


print("Recovered old state:")
print(old_state.values)


# ============================================================
# 12. REPLAY FROM THE SELECTED CHECKPOINT
# ============================================================
# Now we use the selected checkpoint as the starting point
# for replay.
#
# LangGraph will continue execution from that historical
# checkpoint.
#
# Nodes that were already completed before the checkpoint
# are not executed again.
#
# Nodes after the checkpoint can execute again.

print("\n========== REPLAY FROM SELECTED CHECKPOINT ==========\n")

replay_result = app.invoke(
    None,
    old_config
)


# Print the result of the replay

print("\nReplay result:")
print(replay_result)