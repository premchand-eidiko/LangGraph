from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

class State(TypedDict):
    topic: str
    summary: str
    advantages: str
    disadvantages: str
    final_answer: str

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=300
)

def summary_node(state: State):
    print("Summary LLM executing...")
    response = llm.invoke(f"Give a short summary of {state['topic']}.")
    return { "summary": response.content }

def advantages_node(state: State):
    print("Advantages LLM executing...")
    response = llm.invoke( f"List 3 advantages of {state['topic']}.")
    return { "advantages": response.content }

def disadvantages_node(state: State):
    print("Disadvantages LLM executing...")
    response = llm.invoke( f"List 3 disadvantages of {state['topic']}." )
    return { "disadvantages": response.content }

def combine_node(state: State):
    print("Combining results...")
    final_answer = f"""Topic: {state['topic']}\n SUMMARY:{state['summary']}\n ADVANTAGES:{state['advantages']}\n DISADVANTAGES:{state['disadvantages']}"""
    return { "final_answer": final_answer }

graph = StateGraph(State)

graph.add_node("summary", summary_node)
graph.add_node("advantages", advantages_node)
graph.add_node("disadvantages", disadvantages_node)
graph.add_node("combine", combine_node)

graph.add_edge(START, "summary")
graph.add_edge(START, "advantages")
graph.add_edge(START, "disadvantages")

graph.add_edge("summary", "combine")
graph.add_edge("advantages", "combine")
graph.add_edge("disadvantages", "combine")

graph.add_edge("combine", END)

app = graph.compile()


topic = input("Enter a topic: ")

input_data = {
    "topic": topic,
    "summary": "",
    "advantages": "",
    "disadvantages": "",
    "final_answer": ""
}

result = app.invoke(input_data)

print("\n==============================")
print("FINAL ANSWER")
print("==============================")

print(result["final_answer"])