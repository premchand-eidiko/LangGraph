from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

class State(TypedDict):
    question: str
    route: str
    research: str
    summary: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

def manager_agent(state: State):
    if not state["research"]:
        return {
            "route": "researcher"
        }
    return {  "route": "summarizer" }

def researcher_agent(state: State):
    prompt = f"""
    You are a Researcher Agent.
    Research the following topic and provide
    useful factual information.
    Topic:
    {state["question"]}
    """

    response = llm.invoke(prompt)
    return {  "research": response.content }


def summarizer_agent(state: State):
    prompt = f"""
    You are a Summarizer Agent.
    Create a clear and concise summary
    from the research below.
    Research:
    {state["research"]}
    """

    response = llm.invoke(prompt)
    return {  "summary": response.content }

def route_after_manager(state: State):
    return state["route"]

builder = StateGraph(State)

builder.add_node( "manager", manager_agent )
builder.add_node( "researcher", researcher_agent)
builder.add_node( "summarizer", summarizer_agent)


builder.add_edge( START, "manager")
builder.add_conditional_edges(
    "manager",
    route_after_manager,
    {
        "researcher": "researcher",
        "summarizer": "summarizer"
    }
)

builder.add_edge("researcher","manager")
builder.add_edge( "summarizer", END)

app = builder.compile()

question=input("Enter your question: ")

input_data = {
    "question": question,
    "route": "",
    "research": "",
    "summary": ""
}


result = app.invoke(input_data)


print("\n========== QUESTION ==========")
print(result["question"])

print("\n========== RESEARCH ==========")
print(result["research"])

print("\n========== SUMMARY ==========")
print(result["summary"])