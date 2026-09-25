from langchain_groq import ChatGroq

from app.config.settings import settings


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=1000,
    api_key=settings.GROQ_API_KEY,
)


def validator_agent(
    user_query: str,
    research_results: list,
) -> dict:

    combined_results = "\n\n".join(
        [
            f"Research Task: {item['task']}\n"
            f"Result:\n{item['result'][:1000]}"
            for item in research_results
        ]
    )

    prompt = f"""
You are a Validator Agent.

User Query:
{user_query}

Research Results:
{combined_results[:3000]}

Determine whether the research is sufficient.

Check:
1. Major aspects covered?
2. Enough evidence?
3. Important claims supported?
4. Important gaps or contradictions?

Return exactly:

STATUS: SUFFICIENT
FEEDBACK: <brief explanation>

OR

STATUS: INSUFFICIENT
FEEDBACK: <specific missing information>

Rules:
- Do not add outside knowledge.
- Do not invent evidence.
- Keep the feedback concise.
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if "STATUS: SUFFICIENT" in content.upper():
        status = "sufficient"
    else:
        status = "insufficient"

    feedback = content.split("FEEDBACK:", 1)[-1].strip()

    return {
        "status": status,
        "feedback": feedback,
    }