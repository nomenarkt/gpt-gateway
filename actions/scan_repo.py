# actions/scan_repo.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_api import scan_repo_tree

router = APIRouter()

class ScanRepoPayload(BaseModel):
    owner: str
    repo: str
    path: str = ""     # Starting point (e.g., backend/)
    branch: str = "main"
    depth: int = 5     # Max depth to recurse

@router.post("")
async def scan_repo(payload: ScanRepoPayload):
    try:
        tree = await scan_repo_tree(
            owner=payload.owner,
            repo=payload.repo,
            path=payload.path,
            branch=payload.branch,
            max_depth=payload.depth
        )
        return {"status": "success", "tree": tree}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
