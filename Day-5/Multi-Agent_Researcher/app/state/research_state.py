from typing import Annotated, TypedDict
import operator


class ResearchState(TypedDict):

    user_query: str

    research_tasks: list[str]

    research_results: Annotated[list, operator.add]

    sources: Annotated[list, operator.add]

    validation_feedback: str

    research_attempts: int

    analysis: str

    final_report: str