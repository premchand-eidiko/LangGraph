#added checkpoints of every node in InMemorySaver
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    name:str
    status:str

def node_1(state:State):
    print("Node_1 Executing")
    state["name"]="prem"
    return state

def node_2(state:State):
    print("Node_2 Executing")
    state["status"]="completed"
    return state        

checkpointer=InMemorySaver()

graph=StateGraph(State)

graph.add_node("node_1",node_1)
graph.add_node("node_2",node_2)

graph.add_edge(START,"node_1")
graph.add_edge("node_1","node_2")
graph.add_edge("node_2",END)

app=graph.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "user-1"
    }
}

result=app.invoke(
        {
        "name": "",
        "status": ""
        },
        config
    )

state=graph.get_state(config)
print(state)   