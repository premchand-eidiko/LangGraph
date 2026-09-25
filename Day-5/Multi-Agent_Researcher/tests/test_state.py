from app.state.research_state import ResearchState


def test_research_state_has_required_fields():

    annotations = ResearchState.__annotations__

    required_fields = [
        "user_query",
        "research_tasks",
        "research_results",
        "sources",
        "validation_feedback",
        "research_attempts",
        "analysis",
        "final_report",
    ]

    for field in required_fields:
        assert field in annotations