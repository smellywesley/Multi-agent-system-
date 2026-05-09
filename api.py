import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from multi_agent_system.config import get_settings
from multi_agent_system.workflows.review_workflow import ReviewWorkflow

app = FastAPI()

# Allow your local Next.js app to talk to Hugging Face
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    task: str

@app.post("/api/research")
def api_research(request: ResearchRequest):
    try:
        workflow = ReviewWorkflow()
        result = workflow.run(task=request.task)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Hugging Face MUST run on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
