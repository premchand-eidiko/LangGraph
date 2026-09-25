from unittest.mock import MagicMock

import app.agents.validator as validator


def test_validator_sufficient(
    monkeypatch,
):

    response = MagicMock()

    response.content = (
        "STATUS: SUFFICIENT\n"
        "FEEDBACK: Research covers the major aspects."
    )

    monkeypatch.setattr(
        validator.llm,
        "invoke",
        lambda prompt: response,
    )

    result = validator.validator_agent(
        "Explain RAG",
        [
            {
                "task": "RAG basics",
                "result": "RAG retrieves documents.",
            }
        ],
    )

    assert result["status"] == "sufficient"
    assert "Research covers" in result["feedback"]