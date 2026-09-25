from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from api.schemas import (
    ResearchRequest,
    ResearchResponse,
)

from app.graph.workflow import graph

from app.memory.memory import (
    get_thread_state,
    get_thread_history,
)

from app.streaming.node_stream import (
    stream_research,
)

from app.streaming.token_stream import (
    stream_final_report,
)

from app.utils.logger import logger


router = APIRouter()


def create_initial_state(
    query: str,
):

    return {
        "user_query": query,
        "research_tasks": [],
        "research_results": [],
        "sources": [],
        "validation_feedback": "",
        "research_attempts": 0,
        "analysis": "",
        "final_report": "",
    }


@router.post(
    "/research",
    response_model=ResearchResponse,
)
def research(
    request: ResearchRequest,
):

    logger.info(
        "Research request | thread=%s",
        request.thread_id,
    )

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    initial_state = create_initial_state(
        request.query
    )

    result = graph.invoke(
        initial_state,
        config=config,
    )

    return ResearchResponse(
        thread_id=request.thread_id,
        final_report=result[
            "final_report"
        ],
    )


@router.post(
    "/research/stream",
)
def research_stream(
    request: ResearchRequest,
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    initial_state = create_initial_state(
        request.query
    )

    return StreamingResponse(
        stream_research(
            initial_state,
            config,
        ),
        media_type="text/plain",
    )


@router.post(
    "/research/token-stream",
)
def research_token_stream(
    request: ResearchRequest,
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    initial_state = create_initial_state(
        request.query
    )

    return StreamingResponse(
        stream_final_report(
            initial_state,
            config,
        ),
        media_type="text/plain",
    )


@router.post(
    "/research/orchestration-stream",
)
def research_orchestration_stream(
    request: ResearchRequest,
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    initial_state = create_initial_state(
        request.query
    )

    return StreamingResponse(
        stream_research(
            initial_state,
            config,
        ),
        media_type="text/plain",
    )


@router.get(
    "/research/{thread_id}/state",
)
def research_state(
    thread_id: str,
):

    state = get_thread_state(
        thread_id
    )

    return {
        "thread_id": thread_id,
        "state": state.values,
    }


@router.get(
    "/research/{thread_id}/history",
)
def research_history(
    thread_id: str,
):

    history = get_thread_history(
        thread_id
    )

    return {
        "thread_id": thread_id,
        "history": history,
    }