from langchain_groq import ChatGroq

from app.config.settings import settings
from app.utils.retry import retry_call


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=1000,
    api_key=settings.GROQ_API_KEY,
)


def manager_agent(
    user_query: str,
) -> list[str]:

    prompt = f"""
You are the Manager Agent of a research system.

User Query:
{user_query}

Break the query into 3 independent research tasks.

Return only the research tasks, one per line.
"""

    response = retry_call(
        llm.invoke,
        prompt,
        attempts=3,
        delay=2,
    )

    tasks = [
        task.strip("- ").strip()
        for task in response.content.split("\n")
        if task.strip()
    ]

    return tasks[:3]


def retry_manager_agent(
    user_query: str,
    feedback: str,
) -> list[str]:

    prompt = f"""
You are the Manager Agent in a research system.

User Query:
{user_query}

Previous Research Validation:
{feedback}

The previous research was insufficient.

Create 2 new research tasks specifically targeting
the missing information identified by the validator.

Return only the new research tasks, one per line.

Do not repeat the previous research unnecessarily.
"""

    response = retry_call(
        llm.invoke,
        prompt,
        attempts=3,
        delay=2,
    )

    tasks = [
        task.strip("- ").strip()
        for task in response.content.split("\n")
        if task.strip()
    ]

    return tasks[:2]