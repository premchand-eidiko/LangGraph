# Multi-Agent Research Assistant

A production-oriented research assistant built with LangGraph.

## Architecture
s
User
→ FastAPI
→ Manager Agent
→ Researcher Agents
→ Validator
→ Analyst
→ Summarizer
→ Final Research Report

## Main Concepts

- LangGraph
- Multi-Agent Systems
- Manager Agent
- Researcher Agents
- Parallel Research
- Annotated State
- Reducers
- Validation
- Reflection Loop
- Memory
- Checkpointing
- PostgreSQL
- Streaming
- FastAPI
- Tool Calling
- Logging
- Error Handling
- Retry
- Testing

## Run

```bash
source venv/bin/activate
uvicorn app.main:app --reload