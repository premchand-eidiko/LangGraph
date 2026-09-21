#Conditional logic-file contains decison inside the node 
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

def send_decision(state:State):
    print(f"\nApplication Decision:  {state['decision']}")      
    return {}  

graph=StateGraph(State)    

graph.add_node("receive_application",receive_application)
graph.add_node("screen_resume",screen_resume)
graph.add_node("send_decision",send_decision)

graph.add_edge(START,"receive_application")
graph.add_edge("receive_application","screen_resume")
graph.add_edge("screen_resume","send_decision")
graph.add_edge("send_decision",END)

app=graph.compile()

result = app.invoke({
    "name": "Prem",
    "role": "AI Engineer",
    "experience_yrs": 2,
    "decision": ""
})

print("\nFinal State:")
print(result)