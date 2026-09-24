from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

load_dotenv()


# -----------------------------
# 1. Define State
# -----------------------------

class State(TypedDict):
    question: str
    answer: str


# -----------------------------
# 2. Create LLM
# -----------------------------

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=500
)


# -----------------------------
# 3. Create Node
# -----------------------------

def answer_node(state: State):

    writer = get_stream_writer()

    answer = ""

    print("\nAnswer:\n")

    # Stream tokens/chunks from LLM
    for chunk in llm.stream(state["question"]):

        if chunk.content:

            print(chunk.content, end="", flush=True)

            # Send chunk to LangGraph stream
            writer(chunk.content)

            answer += chunk.content

    return {
        "answer": answer
    }


# -----------------------------
# 4. Create Graph
# -----------------------------

graph = StateGraph(State)

graph.add_node("answer", answer_node)

graph.add_edge(START, "answer")
graph.add_edge("answer", END)


# -----------------------------
# 5. Compile Graph
# -----------------------------

app = graph.compile()


# -----------------------------
# 6. Get User Input
# -----------------------------

question = input("Enter your question: ")

input_data = {
    "question": question,
    "answer": ""
}


# -----------------------------
# 7. Token Streaming
# -----------------------------

print("\nStarting token streaming...\n")

for chunk in app.stream(
    input_data,
    stream_mode="custom"
):
    print(chunk, end="", flush=True)


print("\n\nDone.")