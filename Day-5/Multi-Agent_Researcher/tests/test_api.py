from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from api.routes import router


def test_api_router_exists():

    routes = [
        route.path
        for route in router.routes
    ]

    assert "/research" in routes
    assert "/research/stream" in routes
    assert "/research/token-stream" in routes
    assert (
        "/research/{thread_id}/state"
        in routes
    )
    assert (
        "/research/{thread_id}/history"
        in routes
    )