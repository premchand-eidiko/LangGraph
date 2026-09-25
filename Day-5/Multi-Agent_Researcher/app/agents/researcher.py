from langchain_groq import ChatGroq

from app.config.settings import settings
from app.tools.search_tool import search_web
from app.tools.source_reader import read_source
from app.utils.retry import retry_call
from app.utils.logger import logger


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=1500,
    api_key=settings.GROQ_API_KEY,
)


def researcher_agent(
    task: str,
) -> dict:

    logger.info(
        "Researcher started | task=%s",
        task,
    )

    search_results = search_web(task)

    source_text = read_source.invoke(
        {
            "source_text": str(
                search_results
            )
        }
    )

    bounded_source_text = source_text[:5000]

    prompt = f"""
You are a Researcher Agent.

Research Task:
{task}

Web Search Results:
{bounded_source_text}

Instructions:

1. Extract the most important factual findings.
2. Use only information present in the search results.
3. Do not invent facts or statistics.
4. Do not invent URLs.
5. Preserve actual source titles and URLs when available.
6. Keep the response concise.
7. If evidence is insufficient, say so.

Return:

FINDINGS:
<concise factual findings>

SOURCES:
<actual source titles and URLs>
"""

    response = retry_call(
        llm.invoke,
        prompt,
        attempts=3,
        delay=2,
    )

    logger.info(
        "Researcher completed | task=%s",
        task,
    )

    return {
        "task": task,
        "result": response.content,
        "sources": bounded_source_text,
    }