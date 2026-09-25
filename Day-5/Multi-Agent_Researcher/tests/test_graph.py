from app.graph.workflow import graph


def test_graph_nodes_exist():

    graph_nodes = graph.get_graph().nodes

    expected_nodes = {
        "manager",
        "retry_manager",
        "researcher",
        "validator",
        "analyst",
        "summarizer",
    }

    for node in expected_nodes:
        assert node in graph_nodes


def test_graph_has_research_flow():

    graph_edges = graph.get_graph().edges

    edge_pairs = {
        (
            edge.source,
            edge.target,
        )
        for edge in graph_edges
    }

    assert (
        "manager",
        "researcher",
    ) in edge_pairs

    assert (
        "researcher",
        "validator",
    ) in edge_pairs

    assert (
        "validator",
        "analyst",
    ) in edge_pairs

    assert (
        "analyst",
        "summarizer",
    ) in edge_pairs