"""FastAPI gateway for Vercel deployment."""

from fastapi import FastAPI
from pydantic import BaseModel

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
def research(request: ResearchRequest) -> dict[str, object]:
    """Run review workflow for a research task."""
    workflow = ReviewWorkflow()
    result = workflow.run(task=request.task)
    return result.model_dump()
