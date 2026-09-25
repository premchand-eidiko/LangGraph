from app.graph.workflow import graph


def get_thread_state(
    thread_id: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = graph.get_state(
        config
    )

    return state


def get_thread_history(
    thread_id: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    history = []

    for snapshot in graph.get_state_history(
        config
    ):

        history.append(
            {
                "checkpoint_id": (
                    snapshot.config
                    .get("configurable", {})
                    .get("checkpoint_id")
                ),
                "created_at": (
                    snapshot.created_at
                ),
                "step": (
                    snapshot.metadata.get(
                        "step"
                    )
                    if snapshot.metadata
                    else None
                ),
                "state": snapshot.values,
            }
        )

    return history