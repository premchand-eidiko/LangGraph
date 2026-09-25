from app.graph.workflow import graph
from app.streaming.progress import format_progress


def stream_research(initial_state, config):

    for event in graph.stream(
        initial_state,
        config=config,
        stream_mode="updates",
    ):

        progress = format_progress(event)

        if progress:
            yield progress