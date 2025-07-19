# actions/write_file.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.github_api import get_file_sha, write_file_to_repo
import base64

router = APIRouter()

class WriteFilePayload(BaseModel):
    owner: str
    repo: str
    branch: str
    path: str  # Path to the file within the repo
    content: str  # Raw string (will be base64-encoded)
    message: str  # Commit message
    author_name: str = "GPT Agent"
    author_email: str = "gpt-agent@nomena.dev"

@router.put("")
async def write_file(payload: WriteFilePayload):
    try:
        # Check if file exists (to get SHA for update)
        sha = await get_file_sha(
            owner=payload.owner,
            repo=payload.repo,
            path=payload.path,
            branch=payload.branch
        )

        # Encode content to Base64
        b64_content = base64.b64encode(payload.content.encode()).decode()

        # Write the file
        response = await write_file_to_repo(
            owner=payload.owner,
            repo=payload.repo,
            branch=payload.branch,
            path=payload.path,
            content=b64_content,
            message=payload.message,
            sha=sha,
            author={
                "name": payload.author_name,
                "email": payload.author_email
            }
        )
        return {"status": "success", "result": response}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
