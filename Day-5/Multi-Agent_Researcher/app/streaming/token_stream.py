from app.config.settings import settings
from app.graph.workflow import graph
from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=2000,
    api_key=settings.GROQ_API_KEY,
)


def stream_tokens(prompt: str):

    for chunk in llm.stream(prompt):

        if chunk.content:
            yield chunk.content


def stream_final_report(
    initial_state,
    config,
):

    streaming_config = {
        **config,
        "configurable": {
            **config.get("configurable", {}),
            "stream_final_report": True,
        },
    }

    for chunk in graph.stream(
        initial_state,
        config=streaming_config,
        stream_mode="custom",
    ):

        if chunk:
            yield chunk