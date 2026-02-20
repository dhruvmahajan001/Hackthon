from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.repo_service import RepoService
from agents.orchestrator import Orchestrator


class RunAgentRequest(BaseModel):
    repo_url: str
    team_name: str
    leader_name: str
    retry_limit: Optional[int] = 5  # ✅ Configurable retry


app = FastAPI(title="Autonomous CI Repair Agent")

repo_service = RepoService()


@app.post("/run-agent")
async def run_agent(payload: RunAgentRequest):
    try:
        clone_path = repo_service.clone_repo(payload.repo_url)

        orchestrator = Orchestrator(
            repo_path=clone_path,
            team_name=payload.team_name,
            leader_name=payload.leader_name,
            max_retry=payload.retry_limit,   # ✅ Pass retry
        )

        result = orchestrator.run()

        return {
            "status": "success",
            "result": result,
        }

    except Exception as e:
        raise e



@app.get("/health")
async def health():
    return {"status": "ok"}
