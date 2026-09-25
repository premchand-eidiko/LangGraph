from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str
    thread_id: str = "default"


class ResearchResponse(BaseModel):
    thread_id: str
    final_report: str