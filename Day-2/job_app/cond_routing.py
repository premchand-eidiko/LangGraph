#Conditional routing-graph changes its path based on State 
from typing import TypedDict
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    name:str
    role:str
    experience_yrs:int
    decision:str

def receive_application(state:State):
    print(f"Application received for {state['name']}")
    return {}

def screen_resume(state:State):
    if state["experience_yrs"]>2:
        return { "decision" : "Selected" }
    else:
        return { "decision" : "Rejected" }    

def route_decision(state:State):
    if state["decision"]=="Selected":
        return "send_selected"
    else:
        return "send_rejected"    

def send_selected(state: State):
    print("\nApplication Decision: Selected")
    return {}

def send_rejected(state: State):
    print("\nApplication Decision: Rejected")
    return {}

graph=StateGraph(State)    

graph.add_node("receive_application",receive_application)
graph.add_node("screen_resume",screen_resume)
graph.add_node("send_selected",send_selected)
graph.add_node("send_rejected",send_rejected)

graph.add_edge(START,"receive_application")
graph.add_edge("receive_application","screen_resume")
graph.add_conditional_edges("screen_resume",route_decision)
graph.add_edge("send_selected", END)
graph.add_edge("send_rejected", END)

app=graph.compile()

result = app.invoke({
    "name": "Prem",
    "role": "AI Engineer",
    "experience_yrs": 5,
    "decision": ""
})

print("\nFinal State:")
print(result)