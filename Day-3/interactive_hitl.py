#Human in the loop with Conditional-Routing
#human in the loop with dynamic inputs through Terminal

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


# -----------------------------------
# 1. State
# -----------------------------------

class State(TypedDict):
    employee: str
    amount: int
    status: str
    approval: str


# -----------------------------------
# 2. Submit Request
# -----------------------------------

def submit_request(state: State):

    print("\nSubmitting purchase request...")

    state["status"] = "submitted"

    return state


# -----------------------------------
# 3. Validate Request
# -----------------------------------

def validate_request(state: State):

    print("Validating purchase request...")

    if state["amount"] <= 0:
        state["status"] = "invalid"
    else:
        state["status"] = "pending_approval"

    return state


# -----------------------------------
# 4. Human Approval
# -----------------------------------

def human_approval(state: State):

    approval = interrupt(
        f"Approve purchase request of ₹{state['amount']} "
        f"for employee {state['employee']}? (yes/no)"
    )

    if approval.lower() == "yes":
        state["approval"] = "approved"
    else:
        state["approval"] = "rejected"

    return state


# -----------------------------------
# 5. Route After Approval
# -----------------------------------

def route_after_approval(state: State):

    if state["approval"] == "approved":
        return "process_request"

    return "reject_request"


# -----------------------------------
# 6. Process Request
# -----------------------------------

def process_request(state: State):

    print("\nProcessing approved purchase request...")

    state["status"] = "processed"

    return state


# -----------------------------------
# 7. Reject Request
# -----------------------------------

def reject_request(state: State):

    print("\nPurchase request rejected.")

    state["status"] = "rejected"

    return state


# -----------------------------------
# 8. Create Graph
# -----------------------------------

graph = StateGraph(State)


# -----------------------------------
# 9. Add Nodes
# -----------------------------------

graph.add_node("submit_request", submit_request)

graph.add_node("validate_request", validate_request)

graph.add_node("human_approval", human_approval)

graph.add_node("process_request", process_request)

graph.add_node("reject_request", reject_request)


# -----------------------------------
# 10. Add Edges
# -----------------------------------

graph.add_edge(
    START,
    "submit_request"
)

graph.add_edge(
    "submit_request",
    "validate_request"
)

graph.add_edge(
    "validate_request",
    "human_approval"
)


# -----------------------------------
# 11. Conditional Routing
# -----------------------------------

graph.add_conditional_edges(
    "human_approval",
    route_after_approval,
    {
        "process_request": "process_request",
        "reject_request": "reject_request"
    }
)


# -----------------------------------
# 12. End Edges
# -----------------------------------

graph.add_edge(
    "process_request",
    END
)

graph.add_edge(
    "reject_request",
    END
)


# -----------------------------------
# 13. Checkpointer
# -----------------------------------

checkpointer = InMemorySaver()


# -----------------------------------
# 14. Compile
# -----------------------------------

app = graph.compile(
    checkpointer=checkpointer
)


# -----------------------------------
# 15. Get User Input
# -----------------------------------

print("\n==============================")
print("   APPROVAL WORKFLOW SYSTEM")
print("==============================")

employee = input("\nEnter employee name: ")

while True:
    try:
        amount = int(input("Enter purchase amount: "))
        break
    except ValueError:
        print("Please enter a valid number.")


# -----------------------------------
# 16. Thread Configuration
# -----------------------------------

config = {
    "configurable": {
        "thread_id": "purchase-request-1"
    }
}


# -----------------------------------
# 17. Start Workflow
# -----------------------------------

result = app.invoke(
    {
        "employee": employee,
        "amount": amount,
        "status": "",
        "approval": ""
    },
    config
)


# -----------------------------------
# 18. Display Interrupt
# -----------------------------------

print("\nWorkflow paused for human approval.")

print(result["__interrupt__"][0].value)


# -----------------------------------
# 19. Get Human Decision
# -----------------------------------

while True:

    decision = input("Enter your decision (yes/no): ").lower().strip()

    if decision in ["yes", "no"]:
        break

    print("Please enter only 'yes' or 'no'.")


# -----------------------------------
# 20. Resume Workflow
# -----------------------------------

result = app.invoke(
    Command(resume=decision),
    config
)


# -----------------------------------
# 21. Final Result
# -----------------------------------

print("\n==============================")
print("       FINAL RESULT")
print("==============================")

print(f"Employee : {result['employee']}")
print(f"Amount   : ₹{result['amount']}")
print(f"Approval : {result['approval']}")
print(f"Status   : {result['status']}")