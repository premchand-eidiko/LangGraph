from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    acc_holder:str
    balance:float
    trans_amount:float
    status:str
    message:str

def validate_trans(state:State):
    print("\nValidating the transaction...")
    if(state["trans_amount"]<=0):
        state["status"]="failed"
        state["message"]="Transaction amount must be greater than zero."
        print("\nTransaction failed: Amount must be greater than zero.")
        return state
    else:
        print("\nTransaction validated successfully.")
        return state


def route_trans(state:State):
    print("\nRouting the transaction...")
    if(state["trans_amount"]>state["balance"]):
        return "insufficient_funds"
    elif(state["trans_amount"]>100000):
        return "flag_for_review"
    else:
        return "process_trans"    

def insufficient_funds(state:State):
    print("\nInsufficient funds for the transaction.")
    state["status"] = "failed"
    state["message"] = "Transaction failed due to insufficient funds."
    return state

def flag_for_review(state:State):
    print("\nTransaction flagged for review.")
    state["status"] = "pending_review"
    state["message"] = "Transaction flagged for review due to high amount."
    return state

def process_trans(state:State):
      state["balance"]-=state["trans_amount"]
      state["status"]="success"
      state["message"]="Transaction processed successfully."
      print("\nTransaction processed successfully.")
      return state              

graph=StateGraph(State)

graph.add_node("validate_trans", validate_trans)
graph.add_node("route_trans", route_trans)
graph.add_node("insufficient_funds", insufficient_funds)
graph.add_node("flag_for_review", flag_for_review)
graph.add_node("process_trans", process_trans)

graph.add_edge(START, "validate_trans")
graph.add_conditional_edges(
    "validate_trans", 
    route_trans,
    {
        "insufficient_funds": "insufficient_funds",
        "flag_for_review": "flag_for_review",
        "process_trans": "process_trans"
    }
    )
graph.add_edge("insufficient_funds", END)
graph.add_edge("flag_for_review", END) 
graph.add_edge("process_trans", END)   

app=graph.compile()

result=app.invoke({
    "acc_holder":"Prem",
    "balance":200000.0,
    "trans_amount":50000.0,
    "status":"",
    "message":""
})

print("\nFinal State:")
print(result)