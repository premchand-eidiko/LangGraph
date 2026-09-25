def route_after_validation(state):

    attempts = state.get("research_attempts", 0)

    if (
        state["validation_feedback"].startswith("INSUFFICIENT")
        and attempts < 2
    ):
        return "research"

    return "analysis"