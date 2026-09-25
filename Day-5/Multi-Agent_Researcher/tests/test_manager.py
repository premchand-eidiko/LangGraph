from unittest.mock import MagicMock

import app.agents.manager as manager


def test_manager_creates_tasks(
    monkeypatch,
):

    response = MagicMock()

    response.content = (
        "Research RAG fundamentals\n"
        "Research RAG architecture\n"
        "Research RAG benefits"
    )

    monkeypatch.setattr(
        manager.llm,
        "invoke",
        lambda prompt: response,
    )

    tasks = manager.manager_agent(
        "Explain RAG"
    )

    assert len(tasks) == 3
    assert "Research RAG fundamentals" in tasks