from unittest.mock import MagicMock

import app.agents.researcher as researcher


def test_researcher_agent(
    monkeypatch,
):

    monkeypatch.setattr(
        researcher,
        "search_web",
        lambda task: (
            "Title: RAG Documentation\n"
            "URL: https://example.com\n"
            "Content: RAG information"
        ),
    )

    reader = MagicMock()

    reader.invoke.return_value = (
        "RAG information"
    )

    monkeypatch.setattr(
        researcher,
        "read_source",
        reader,
    )

    response = MagicMock()

    response.content = (
        "FINDINGS:\n"
        "RAG retrieves relevant external information.\n\n"
        "SOURCES:\n"
        "https://example.com"
    )

    monkeypatch.setattr(
        researcher.llm,
        "invoke",
        lambda prompt: response,
    )

    result = researcher.researcher_agent(
        "Research RAG"
    )

    assert result["task"] == "Research RAG"
    assert "FINDINGS" in result["result"]
    assert result["sources"]