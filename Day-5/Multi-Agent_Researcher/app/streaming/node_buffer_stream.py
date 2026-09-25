from app.graph.workflow import graph


def stream_node_updates(initial_state, config):

    for event in graph.stream(
        initial_state,
        config=config,
        stream_mode="updates",
    ):
        yield event