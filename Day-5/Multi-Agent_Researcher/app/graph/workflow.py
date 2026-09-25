from langgraph.graph import StateGraph, START, END

from app.database.postgres import create_checkpointer
from app.state.research_state import ResearchState

from app.graph.nodes import (
    manager_node,
    retry_manager_node,
    researcher_node,
    validator_node,
    analyst_node,
    summarizer_node,
)

from app.graph.routing import route_after_validation


def build_graph():

    workflow = StateGraph(ResearchState)

    workflow.add_node(
        "manager",
        manager_node,
    )

    workflow.add_node(
        "retry_manager",
        retry_manager_node,
    )

    workflow.add_node(
        "researcher",
        researcher_node,
    )

    workflow.add_node(
        "validator",
        validator_node,
    )

    workflow.add_node(
        "analyst",
        analyst_node,
    )

    workflow.add_node(
        "summarizer",
        summarizer_node,
    )

    workflow.add_edge(
        START,
        "manager",
    )

    workflow.add_edge(
        "manager",
        "researcher",
    )

    workflow.add_edge(
        "researcher",
        "validator",
    )

    workflow.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "research": "retry_manager",
            "analysis": "analyst",
        },
    )

    workflow.add_edge(
        "retry_manager",
        "researcher",
    )

    workflow.add_edge(
        "analyst",
        "summarizer",
    )

    workflow.add_edge(
        "summarizer",
        END,
    )

    checkpointer = create_checkpointer()

    return workflow.compile(
        checkpointer=checkpointer
    )


graph = build_graph()