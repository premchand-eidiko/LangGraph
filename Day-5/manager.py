from typing import TypedDict, Literal

from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END


# ==========================================
# 1. Load environment
# ==========================================

load_dotenv()


# ==========================================
# 2. State
# ==========================================

class State(TypedDict):
    question: str
    route: str
    result: str


# ==========================================
# 3. Manager decision schema
# ==========================================

class ManagerDecision(BaseModel):
    next_agent: Literal["researcher", "summarizer"]


# ==========================================
# 4. LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


manager_llm = llm.with_structured_output(
    ManagerDecision
)


# ==========================================
# 5. Manager Agent
# ==========================================

def manager_agent(state: State):

    prompt = f"""
    You are the Manager Agent.

    Decide which specialist should handle
    the user's request.

    Available specialists:

    researcher:
    Handles research, information gathering,
    investigation, and explanations.

    summarizer:
    Handles requests to summarize existing
    information.

    User request:
    {state["question"]}

    Choose the most appropriate specialist.
    """

    decision = manager_llm.invoke(prompt)

    return {
        "route": decision.next_agent
    }


# ==========================================
# 6. Researcher Agent
# ==========================================

def researcher_agent(state: State):

    return {
        "result": (
            f"Researcher Agent selected for: "
            f"{state['question']}"
        )
    }


# ==========================================
# 7. Summarizer Agent
# ==========================================

def summarizer_agent(state: State):

    return {
        "result": (
            f"Summarizer Agent selected for: "
            f"{state['question']}"
        )
    }


# ==========================================
# 8. Router
# ==========================================

def route_after_manager(state: State):

    return state["route"]


# ==========================================
# 9. Build Graph
# ==========================================

builder = StateGraph(State)

builder.add_node("manager", manager_agent)
builder.add_node("researcher", researcher_agent)
builder.add_node("summarizer", summarizer_agent)


# START → Manager

builder.add_edge(
    START,
    "manager"
)


# Manager → appropriate specialist

builder.add_conditional_edges(
    "manager",
    route_after_manager,
    {
        "researcher": "researcher",
        "summarizer": "summarizer"
    }
)


# Specialists → END

builder.add_edge(
    "researcher",
    END
)

builder.add_edge(
    "summarizer",
    END
)


# ==========================================
# 10. Compile
# ==========================================

app = builder.compile()


# ==========================================
# 11. Test
# ==========================================

input_data = {
    "question": "I want to learn about LangGraph but as short as possible of whole content",
    "route": "",
    "result": ""
}

result = app.invoke(input_data)


# ==========================================
# 12. Output
# ==========================================

print("\nQuestion:")
print(result["question"])

print("\nManager Decision:")
print(result["route"])

print("\nResult:")
print(result["result"])