# actions/list_files.py

from fastapi import APIRouter, HTTPException, Query
from services.github_api import list_files_in_path

router = APIRouter()

@router.get("")
async def list_files(
    owner: str = Query(..., description="GitHub username or organization"),
    repo: str = Query(..., description="GitHub repository name"),
    path: str = Query("", description="Path inside the repository"),
    branch: str = Query("main", description="Branch to scan")
):
    try:
        files = await list_files_in_path(owner=owner, repo=repo, path=path, branch=branch)
        return {"status": "success", "path": path, "files": files}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
