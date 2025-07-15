# services/github_api.py

import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("Missing GITHUB_TOKEN in environment")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


async def get_file_sha(owner: str, repo: str, path: str, branch: str) -> str:
    """
    Return the SHA of a file if it exists on the specified branch.
    Required for updating an existing file on GitHub.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code == 404:
            return None  # File does not exist (new file)
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get file SHA")

        data = response.json()
        return data.get("sha")


async def write_file_to_repo(
    owner: str,
    repo: str,
    branch: str,
    path: str,
    content: str,
    message: str,
    sha: str = None,
    author: dict = None,
):
    """
    Create or update a file in a given repo and branch.
    If SHA is provided, it's treated as an update; otherwise, a new file.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"

    payload = {
        "message": message,
        "content": content,
        "branch": branch,
    }

    if sha:
        payload["sha"] = sha
    if author:
        payload["committer"] = {
            "name": author.get("name", "GPT Agent"),
            "email": author.get("email", "gpt-agent@nomena.dev")
        }

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=HEADERS, json=payload)

        if response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to write file: {response.json().get('message', 'Unknown error')}"
            )

        return response.json()


async def list_files_in_path(owner: str, repo: str, path: str, branch: str = "main") -> list:
    """
    List all files and directories under a given path on a specified branch.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to list files in {path}"
            )

        return response.json()


async def scan_repo_tree(owner: str, repo: str, path: str, branch: str = "main", max_depth: int = 5, current_depth: int = 0) -> list:
    """
    Recursively scan a GitHub repo path up to a given depth.
    Returns a nested list of files and folders.
    """
    if current_depth > max_depth:
        return []

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to read path: {path}")

        items = response.json()
        if not isinstance(items, list):
            return []

        result = []
        for item in items:
            entry = {
                "name": item["name"],
                "path": item["path"],
                "type": item["type"]
            }

            if item["type"] == "dir":
                entry["children"] = await scan_repo_tree(
                    owner, repo, path=item["path"],
                    branch=branch,
                    max_depth=max_depth,
                    current_depth=current_depth + 1
                )

            result.append(entry)

        return result
