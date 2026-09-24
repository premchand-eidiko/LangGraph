from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

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
    temperature=0
)


# -----------------------------
# 3. Create Node
# -----------------------------

def answer_node(state: State):

    print("\nAnswer:\n")

    return {
        "answer": llm.invoke(state["question"]).content
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
# 7. Stream LLM Messages
# -----------------------------

print("\nStarting message streaming...\n")

for message, metadata in app.stream(
    input_data,
    stream_mode="messages"
):

    if message.content:
        print(message.content, end="", flush=True)


print("\n\nDone.")