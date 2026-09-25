from langchain_groq import ChatGroq

from app.config.settings import settings


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=3000,
    api_key=settings.GROQ_API_KEY,
)


def build_summarizer_prompt(
    user_query: str,
    analysis: str,
    sources: list,
) -> str:

    source_text = "\n\n".join(
        [
            f"Task: {item['task']}\n"
            f"Sources:\n{item['sources'][:1200]}"
            for item in sources
        ]
    )

    return f"""
You are the final Summarizer Agent.

User Query:
{user_query}

Research Analysis:
{analysis[:5000]}

Sources:
{source_text[:4000]}

Create a concise final research report.

Include:

1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Important Sources
5. Conclusion

Rules:
- Use only information supported by the research.
- Do not invent facts or statistics.
- Do not invent URLs.
- Preserve actual source URLs when available.
- If sources disagree, mention the disagreement.
- Keep the report concise.
"""


def summarizer_agent(
    user_query: str,
    analysis: str,
    sources: list,
) -> str:

    prompt = build_summarizer_prompt(
        user_query,
        analysis,
        sources,
    )

    response = llm.invoke(prompt)

    return response.content


def stream_summarizer(
    user_query: str,
    analysis: str,
    sources: list,
):

    prompt = build_summarizer_prompt(
        user_query,
        analysis,
        sources,
    )

    for chunk in llm.stream(prompt):

        if chunk.content:
            yield chunk.content