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


# -------------------------
# SUMMARY NODE
# -------------------------

def summary_node(state: State):

    writer = get_stream_writer()

    answer = ""

    for chunk in llm.stream(
        f"Give a short summary of {state['topic']}."
    ):

        if chunk.content:

            writer({
                "node": "summary",
                "content": chunk.content
            })

            answer += chunk.content

    return {
        "summary": answer
    }


# -------------------------
# ADVANTAGES NODE
# -------------------------

def advantages_node(state: State):

    writer = get_stream_writer()

    answer = ""

    for chunk in llm.stream(
        f"List 3 advantages of {state['topic']}."
    ):

        if chunk.content:

            writer({
                "node": "advantages",
                "content": chunk.content
            })

            answer += chunk.content

    return {
        "advantages": answer
    }


# -------------------------
# DISADVANTAGES NODE
# -------------------------

def disadvantages_node(state: State):

    writer = get_stream_writer()

    answer = ""

    for chunk in llm.stream(
        f"List 3 disadvantages of {state['topic']}."
    ):

        if chunk.content:

            writer({
                "node": "disadvantages",
                "content": chunk.content
            })

            answer += chunk.content

    return {
        "disadvantages": answer
    }


# -------------------------
# COMBINE NODE
# -------------------------

def combine_node(state: State):

    final_answer = f"""
==============================
FINAL ANSWER
==============================

Topic:
{state['topic']}

SUMMARY:
{state['summary']}

ADVANTAGES:
{state['advantages']}

DISADVANTAGES:
{state['disadvantages']}
"""

    return {
        "final_answer": final_answer
    }


# -------------------------
# GRAPH
# -------------------------

graph = StateGraph(State)

graph.add_node("summary", summary_node)
graph.add_node("advantages", advantages_node)
graph.add_node("disadvantages", disadvantages_node)
graph.add_node("combine", combine_node)

# Fan-out
graph.add_edge(START, "summary")
graph.add_edge(START, "advantages")
graph.add_edge(START, "disadvantages")

# Fan-in
graph.add_edge("summary", "combine")
graph.add_edge("advantages", "combine")
graph.add_edge("disadvantages", "combine")

graph.add_edge("combine", END)

app = graph.compile()


# -------------------------
# INPUT
# -------------------------

topic = input("Enter a topic: ")

input_data = {
    "topic": topic,
    "summary": "",
    "advantages": "",
    "disadvantages": "",
    "final_answer": ""
}


# -------------------------
# SEPARATE BUFFERS
# -------------------------

buffers = {
    "summary": "",
    "advantages": "",
    "disadvantages": ""
}


print("\nStarting parallel streaming...\n")


# -------------------------
# RECEIVE STREAM
# -------------------------

for chunk in app.stream(
    input_data,
    stream_mode="custom"
):

    node = chunk["node"]
    content = chunk["content"]

    # Store chunk in the correct buffer
    if node in buffers:
        buffers[node] += content


# -------------------------
# DISPLAY SEPARATELY
# -------------------------

print("\n")
print("=" * 50)

print("\nSUMMARY")
print("=" * 50)
print(buffers["summary"])

print("\nADVANTAGES")
print("=" * 50)
print(buffers["advantages"])

print("\nDISADVANTAGES")
print("=" * 50)
print(buffers["disadvantages"])


print("\nDone.")