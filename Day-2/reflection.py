from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)

class State(TypedDict):
    question: str
    answer: str
    feedback: str
    iteration: int
    is_good: bool

def generate_answer(state: State):
    iteration = state["iteration"] + 1

    print(f"\nGenerating answer... Iteration {iteration}")

    prompt = f"""
You are a helpful AI assistant.

User question:
{state["question"]}

Previous reflection feedback:
{state["feedback"]}

Generate a clear, accurate and beginner-friendly answer.

If previous feedback is available, improve the answer
based on that feedback.

Do not mention the reflection process in your answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "iteration": iteration
    }

def reflect_answer(state: State):
    print("\nReflecting on the answer...")

    prompt = f"""
You are an expert reviewer.

User question:
{state["question"]}

Generated answer:
{state["answer"]}

Review the answer based on:

1. Accuracy
2. Relevance
3. Clarity
4. Completeness
5. Beginner-friendliness

Respond exactly in this format:

GOOD: YES

FEEDBACK: <short explanation>

If the answer is already good enough, respond:

GOOD: YES

If it needs improvement, respond:

GOOD: NO
"""

    response = llm.invoke(prompt)

    reflection = response.content.strip()

    print("\nReflection:")
    print(reflection)

    if "GOOD: YES" in reflection.upper():
        return {
            "is_good": True,
            "feedback": reflection
        }

    return {
        "is_good": False,
        "feedback": reflection
    }

def route_after_reflection(state: State):
    if state["is_good"]:
        return "success"

    if state["iteration"] >= 3:
        return "success"

    return "improve"

def improve_answer(state: State):
    print("\nImproving answer...")

    prompt = f"""
You are an expert AI assistant.

User question:
{state["question"]}

Current answer:
{state["answer"]}

Reviewer feedback:
{state["feedback"]}

Improve the answer using the reviewer's feedback.

Make the answer:
- Accurate
- Clear
- Relevant
- Beginner-friendly
- Complete

Return only the improved answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }

def success(state: State):
    print("\n" + "=" * 50)
    print("FINAL ANSWER")
    print("=" * 50)
    print(state["answer"])
    print("\nCompleted in:")
    print(f"{state['iteration']} iteration(s)")
    return {}

graph = StateGraph(State)

graph.add_node("generate_answer", generate_answer)
graph.add_node("reflect_answer", reflect_answer)
graph.add_node("improve_answer", improve_answer)
graph.add_node("success", success)

graph.add_edge(START, "generate_answer")
graph.add_edge("generate_answer", "reflect_answer")

graph.add_conditional_edges(
    "reflect_answer",
    route_after_reflection,
    {
        "improve": "improve_answer",
        "success": "success"
    }
)

graph.add_edge("improve_answer", "reflect_answer")
graph.add_edge("success", END)

app = graph.compile()

question = input("\nEnter your question: ")

result = app.invoke({
    "question": question,
    "answer": "",
    "feedback": "",
    "iteration": 0,
    "is_good": False
})

print("\nFinal State:")
print(result)