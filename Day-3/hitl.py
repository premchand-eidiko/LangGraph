#Human in the loop with Conditional-logic(decision in the node)
#Pre-dertemined human in the loop input Command
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt,Command
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    amount: int
    status: str

def prepare_trans(state:State):
    print("Preparing transaction...")
    state["status"] = "prepared"
    return state

def human_approval(state:State):
    approval=interrupt("Approve this transaction")
    if approval=="yes":
        state["status"] = "approved"
    else:
        state["status"] = "rejected"
    return state

def process_trans(state:State):
    print("Processing transaction...")
    state["status"] = "processed"
    return state        

checkpointer=InMemorySaver()
graph = StateGraph(State)  

graph.add_node("prepare_trans",prepare_trans)
graph.add_node("human_approval",human_approval)
graph.add_node("process_trans",process_trans)

graph.add_edge(START,"prepare_trans")
graph.add_edge("prepare_trans","human_approval")
graph.add_edge("human_approval","process_trans")
graph.add_edge("process_trans",END)

app=graph.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "transaction-1"
    }
}

result=app.invoke(
    {
        "amount":10000,
        "status":""
    },config
)

print(result)

result=app.invoke(
    Command(resume="yes"),config
)

print(result)