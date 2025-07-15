# actions/read_file.py

from fastapi import APIRouter, HTTPException, Query
from services.github_api import read_file_content

router = APIRouter()

@router.get("/")
async def read_file(
    owner: str = Query(..., description="GitHub username or organization"),
    repo: str = Query(..., description="GitHub repository name"),
    path: str = Query(..., description="File path inside the repository"),
    branch: str = Query("main", description="Branch name")
):
    try:
        content = await read_file_content(owner, repo, path, branch)
        return {"status": "success", "path": path, "content": content}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
