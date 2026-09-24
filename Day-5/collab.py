from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# 2. State
# ==========================================

class State(TypedDict):
    question: str
    route: str
    research: str
    summary: str


# ==========================================
# 3. LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ==========================================
# 4. Manager Agent
# ==========================================

def manager_agent(state: State):

    # First visit:
    # No research exists yet.
    if not state["research"]:
        return {
            "route": "researcher"
        }

    # Second visit:
    # Research exists, so summarize it.
    return {
        "route": "summarizer"
    }


# ==========================================
# 5. Researcher Agent
# ==========================================

def researcher_agent(state: State):

    prompt = f"""
    You are a Researcher Agent.

    Research the following topic and provide
    useful factual information.

    Topic:
    {state["question"]}
    """

    response = llm.invoke(prompt)

    return {
        "research": response.content
    }


# ==========================================
# 6. Summarizer Agent
# ==========================================

def summarizer_agent(state: State):

    prompt = f"""
    You are a Summarizer Agent.

    Create a clear and concise summary
    from the research below.

    Research:
    {state["research"]}
    """

    response = llm.invoke(prompt)

    return {
        "summary": response.content
    }


# ==========================================
# 7. Routing Function
# ==========================================

def route_after_manager(state: State):

    return state["route"]


# ==========================================
# 8. Build Graph
# ==========================================

builder = StateGraph(State)


# Add agents

builder.add_node(
    "manager",
    manager_agent
)

builder.add_node(
    "researcher",
    researcher_agent
)

builder.add_node(
    "summarizer",
    summarizer_agent
)


# ==========================================
# 9. Graph Connections
# ==========================================

# START → Manager

builder.add_edge(
    START,
    "manager"
)


# Manager → Researcher OR Summarizer

builder.add_conditional_edges(
    "manager",
    route_after_manager,
    {
        "researcher": "researcher",
        "summarizer": "summarizer"
    }
)


# Researcher → Manager

builder.add_edge(
    "researcher",
    "manager"
)


# Summarizer → END

builder.add_edge(
    "summarizer",
    END
)


# ==========================================
# 10. Compile
# ==========================================

app = builder.compile()


# ==========================================
# 11. Input
# ==========================================

input_data = {
    "question": "What is LangGraph and why is it useful?",
    "route": "",
    "research": "",
    "summary": ""
}


# ==========================================
# 12. Run
# ==========================================

result = app.invoke(input_data)


# ==========================================
# 13. Display Result
# ==========================================

print("\n========== QUESTION ==========")
print(result["question"])

print("\n========== RESEARCH ==========")
print(result["research"])

print("\n========== SUMMARY ==========")
print(result["summary"])