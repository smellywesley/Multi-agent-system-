"""FastAPI gateway for Vercel deployment."""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel

from multi_agent_system.config import Settings, get_settings
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

app = FastAPI(title="multi-agent-system")


class ResearchRequest(BaseModel):
    """Incoming research API request."""

    task: str


def verify_api_key(
    x_api_key: Annotated[str, Header(alias="X-API-KEY")],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    """Validate internal API key for protected endpoints."""
    if x_api_key != settings.internal_api_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


@app.get("/health")
def health() -> dict[str, str]:
    """Health endpoint for uptime checks."""
    return {"status": "ok"}


@app.post("/api/research", dependencies=[Depends(verify_api_key)])
def research(request: ResearchRequest) -> dict[str, object]:
    """Run review workflow for a research task."""
    workflow = ReviewWorkflow()
    result = workflow.run(task=request.task)
    return result.model_dump()
