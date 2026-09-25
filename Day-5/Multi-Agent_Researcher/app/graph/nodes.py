from concurrent.futures import ThreadPoolExecutor, as_completed

from langgraph.config import get_stream_writer

from app.agents.manager import (
    manager_agent,
    retry_manager_agent,
)

from app.agents.researcher import researcher_agent

from app.agents.validator import validator_agent

from app.agents.analyst import analyst_agent

from app.agents.summarizer import (
    summarizer_agent,
    stream_summarizer,
)

from app.utils.logger import logger


def manager_node(state):

    logger.info(
        "Manager started | query=%s",
        state["user_query"],
    )

    tasks = manager_agent(
        state["user_query"]
    )

    logger.info(
        "Manager created %d research tasks",
        len(tasks),
    )

    return {
        "research_tasks": tasks,
        "research_attempts": state.get(
            "research_attempts",
            0,
        ) + 1,
    }


def retry_manager_node(state):

    logger.info(
        "Retry manager started | attempt=%s",
        state.get("research_attempts", 0),
    )

    tasks = retry_manager_agent(
        state["user_query"],
        state["validation_feedback"],
    )

    logger.info(
        "Retry manager created %d tasks",
        len(tasks),
    )

    return {
        "research_tasks": tasks,
        "research_attempts": state.get(
            "research_attempts",
            0,
        ) + 1,
    }


def researcher_node(state):

    tasks = state["research_tasks"]

    logger.info(
        "Parallel research started | tasks=%d",
        len(tasks),
    )

    if not tasks:
        return {
            "research_results": [],
            "sources": [],
        }

    results = []

    max_workers = min(
        len(tasks),
        3,
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_map = {
            executor.submit(
                researcher_agent,
                task,
            ): task
            for task in tasks
        }

        for future in as_completed(
            future_map
        ):

            task = future_map[future]

            try:

                result = future.result()

                results.append(result)

                logger.info(
                    "Research completed | task=%s",
                    task,
                )

            except Exception:

                logger.exception(
                    "Research failed | task=%s",
                    task,
                )

                raise

    return {
        "research_results": [
            {
                "task": result["task"],
                "result": result["result"],
            }
            for result in results
        ],
        "sources": [
            {
                "task": result["task"],
                "sources": result["sources"],
            }
            for result in results
        ],
    }


def validator_node(state):

    logger.info(
        "Validator started | results=%d",
        len(state["research_results"]),
    )

    result = validator_agent(
        state["user_query"],
        state["research_results"],
    )

    logger.info(
        "Validator status=%s",
        result["status"],
    )

    return {
        "validation_feedback": (
            f"{result['status'].upper()}: "
            f"{result['feedback']}"
        )
    }


def analyst_node(state):

    logger.info("Analyst started")

    analysis = analyst_agent(
        state["research_results"]
    )

    logger.info("Analyst completed")

    return {
        "analysis": analysis,
    }


def summarizer_node(
    state,
    config=None,
):

    streaming_enabled = (
        config
        and config.get("configurable", {}).get(
            "stream_final_report",
            False,
        )
    )

    logger.info(
        "Summarizer started | streaming=%s",
        streaming_enabled,
    )

    if streaming_enabled:

        writer = get_stream_writer()

        chunks = []

        for chunk in stream_summarizer(
            state["user_query"],
            state["analysis"],
            state["sources"],
        ):

            writer(chunk)

            chunks.append(chunk)

        final_report = "".join(chunks)

    else:

        final_report = summarizer_agent(
            state["user_query"],
            state["analysis"],
            state["sources"],
        )

    logger.info("Summarizer completed")

    return {
        "final_report": final_report,
    }