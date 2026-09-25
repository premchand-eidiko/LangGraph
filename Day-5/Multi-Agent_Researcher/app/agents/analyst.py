from langchain_groq import ChatGroq

from app.config.settings import settings


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=settings.GROQ_API_KEY,
)


def analyst_agent(research_results: list) -> str:

    combined_results = "\n\n".join(
        [
            f"Task: {item['task']}\n"
            f"Result: {item['result'][:2500]}"
            for item in research_results
        ]
    )

    prompt = f"""
You are an Analyst Agent.

Analyze the research results below.

{combined_results[:6000]}

Return only:

IMPORTANT FINDINGS:
<key findings>

PATTERNS:
<common patterns>

CONTRADICTIONS:
<differences or contradictions>

KEY INSIGHT:
<main insight>

Rules:
- Use only the provided research.
- Do not invent facts.
- Keep each section concise.
"""

    response = llm.invoke(prompt)

    return response.content