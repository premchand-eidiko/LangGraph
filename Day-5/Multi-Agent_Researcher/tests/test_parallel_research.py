import app.graph.nodes as nodes


def test_parallel_research(
    monkeypatch,
):

    def fake_researcher(task):

        return {
            "task": task,
            "result": f"Result for {task}",
            "sources": f"Source for {task}",
        }

    monkeypatch.setattr(
        nodes,
        "researcher_agent",
        fake_researcher,
    )

    state = {
        "research_tasks": [
            "Task A",
            "Task B",
            "Task C",
        ]
    }

    result = nodes.researcher_node(
        state
    )

    assert len(
        result["research_results"]
    ) == 3

    assert len(
        result["sources"]
    ) == 3