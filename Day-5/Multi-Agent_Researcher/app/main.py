from fastapi import (
    FastAPI,
    Request,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.utils.errors import (
    ResearchAssistantError,
)

from app.utils.logger import logger

from api.routes import router


app = FastAPI(
    title="Multi-Agent Research Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(
    ResearchAssistantError
)
async def research_assistant_error_handler(
    request: Request,
    exc: ResearchAssistantError,
):

    logger.error(
        "Application error | path=%s | error=%s",
        request.url.path,
        exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
        },
    )


@app.exception_handler(
    Exception
)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):

    logger.exception(
        "Unhandled application error | path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred.",
        },
    )


app.include_router(
    router,
    prefix="/api",
)


@app.get("/")
def root():

    return {
        "application": (
            "Multi-Agent Research Assistant"
        ),
        "status": "running",
    }