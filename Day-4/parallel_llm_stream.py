from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

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
    writer = get_stream_writer()
    answer = ""
    writer("\n\n--- SUMMARY ---\n")
    for chunk in llm.stream(  f"Give a short summary of {state['topic']}." ):
        if chunk.content:
            writer(chunk.content)
            answer += chunk.content
    return {  "summary": answer }


def advantages_node(state: State):
    writer = get_stream_writer()
    answer = ""
    writer("\n\n--- ADVANTAGES ---\n")
    for chunk in llm.stream( f"List 3 advantages of {state['topic']}."  ):
        if chunk.content:
            writer(chunk.content)
            answer += chunk.content
    return { "advantages": answer  }


def disadvantages_node(state: State):
    writer = get_stream_writer()
    answer = ""
    writer("\n\n--- DISADVANTAGES ---\n")
    for chunk in llm.stream(  f"List 3 disadvantages of {state['topic']}." ):
        if chunk.content:
            writer(chunk.content)
            answer += chunk.content
    return { "disadvantages": answer }


def combine_node(state: State):
    writer = get_stream_writer()
    writer("\n\n--- COMBINING RESULTS ---\n")
    final_answer = f"""
    Topic: {state['topic']} \n

    SUMMARY:
    {state['summary']}\n

    ADVANTAGES:
    {state['advantages']}\n

    DISADVANTAGES:
    {state['disadvantages']}\n
    """

    return {  "final_answer": final_answer }


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


print("\nStarting parallel LLM streaming...\n")

for chunk in app.stream( input_data, stream_mode="custom" ):
    print(chunk, end="", flush=True)


print("\n\nDone.")