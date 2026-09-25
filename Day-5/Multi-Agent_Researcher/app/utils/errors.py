class ResearchAssistantError(Exception):
    """Base application error."""


class AgentError(ResearchAssistantError):
    """Agent execution error."""


class ResearchError(ResearchAssistantError):
    """Research execution error."""


class SearchError(ResearchAssistantError):
    """Web search error."""


class ValidationError(ResearchAssistantError):
    """Research validation error."""


class DatabaseError(ResearchAssistantError):
    """Database/checkpointer error."""


class RetryExhaustedError(ResearchAssistantError):
    """Operation failed after all retry attempts."""