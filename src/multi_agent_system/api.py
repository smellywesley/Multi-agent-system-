"""FastAPI gateway for Vercel deployment."""

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

from multi_agent_system.config import get_settings
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

app = FastAPI(title="multi-agent-system")


class ResearchRequest(BaseModel):
    """Incoming research API request."""

    task: str


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint for uptime checks."""
    return {"status": "ok"}


@app.post("/api/research")
def research(request: ResearchRequest, x_api_key: str = Header(default="")) -> dict[str, object]:
    """Run review workflow for a research task."""
    settings = get_settings()
    if x_api_key != settings.internal_api_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    workflow = ReviewWorkflow()
    result = workflow.run(task=request.task)
    return result.model_dump()
