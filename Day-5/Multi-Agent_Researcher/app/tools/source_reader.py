from langchain_core.tools import tool


@tool
def read_source(
    source_text: str,
) -> str:
    """
    Clean and normalize source content
    before it is passed to a research agent.
    """

    if not source_text:
        return "No source content provided."

    cleaned = str(source_text).strip()

    if not cleaned:
        return "No source content provided."

    return cleaned