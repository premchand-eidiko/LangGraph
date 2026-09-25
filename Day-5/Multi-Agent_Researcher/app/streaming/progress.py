def format_progress(event):

    if not isinstance(event, dict):
        return None

    for node_name in event:

        if node_name == "__start__":
            return "Research started\n"

        if node_name == "manager":
            return "Manager created the research plan\n"

        if node_name == "retry_manager":
            return "Manager created additional research tasks\n"

        if node_name == "researcher":
            return "Researcher completed a research task\n"

        if node_name == "validator":
            return "Validator checked the research\n"

        if node_name == "analyst":
            return "Analyst completed the research analysis\n"

        if node_name == "summarizer":
            return "Summarizer generated the final report\n"

    return None