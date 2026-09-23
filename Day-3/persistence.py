from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


class State(TypedDict):
    employee_name: str
    docs_collected: bool
    access_setup: bool
    orientation_scheduled: bool
    status: str


def document_collection(state: State):
    print("\nCollecting employee documents...")
    state["docs_collected"] = True
    state["status"] = "documents_collected"
    return state


def system_access_setup(state: State):
    print("Setting up system access...")
    state["access_setup"] = True
    state["status"] = "access_setup_completed"
    return state


def orientation_scheduling(state: State):
    print("Scheduling employee orientation...")
    state["orientation_scheduled"] = True
    state["status"] = "onboarding_completed"
    return state


graph = StateGraph(State)

graph.add_node("document_collection", document_collection)
graph.add_node("system_access_setup", system_access_setup)
graph.add_node("orientation_scheduling", orientation_scheduling)

graph.add_edge(START, "document_collection")
graph.add_edge("document_collection", "system_access_setup")
graph.add_edge("system_access_setup", "orientation_scheduling")
graph.add_edge("orientation_scheduling", END)


employee_name = input("Enter employee name: ")

thread_id = f"employee-{employee_name.lower().replace(' ', '-')}"

config = {
    "configurable": {
        "thread_id": thread_id
    }
}


initial_state = {
    "employee_name": employee_name,
    "docs_collected": False,
    "access_setup": False,
    "orientation_scheduled": False,
    "status": "onboarding_started"
}


with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:

    app = graph.compile(checkpointer=checkpointer)

    result = app.invoke(
        initial_state,
        config
    )

    saved_state = app.get_state(config)

    print("\n================================")
    print("       SAVED EMPLOYEE STATE")
    print("================================")

    print(saved_state.values)