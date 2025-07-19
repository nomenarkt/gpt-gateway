# services/github_api.py

import os
import base64
import urllib.parse
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


async def get_file_sha(owner: str, repo: str, path: str, branch: str = "main") -> str | None:
    """
    Get SHA of a file at a specific path and branch.
    Returns None if the file does not exist.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get file SHA")

        return response.json().get("sha")


async def write_file_to_repo(
    owner: str,
    repo: str,
    branch: str,
    path: str,
    content: str,
    message: str,
    sha: str | None = None,
    author: dict | None = None,
):
    """
    Create or update a file on GitHub.
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
    List contents of a directory path on GitHub.
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


async def scan_repo_tree(
    owner: str,
    repo: str,
    path: str = "",
    branch: str = "main",
    max_depth: int = 5,
    current_depth: int = 0
) -> list:
    """
    Recursively scan a GitHub repo path up to a given depth.
    Returns a nested list of files and folders.
    """
    if current_depth > max_depth:
        return []


    print(f"📂 Scanning: owner={owner}, repo={repo}, path={path}, depth={current_depth}")

    encoded_path = urllib.parse.quote(path)
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{encoded_path}?ref={branch}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")
    elif response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to read path: {path}")

    items = response.json()
    if not isinstance(items, list):
        return []

    result = []
    for item in items:
        entry = {
            "name": item["name"],
            "path": item["path"],
            "type": item["type"],
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


async def read_file_content(owner: str, repo: str, path: str, branch: str = "main") -> str:
    """
    Read and decode a file's base64 content from GitHub.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to read file: {path}"
            )

        data = response.json()
        content = data.get("content", "")
        if data.get("encoding") != "base64":
            raise HTTPException(status_code=400, detail="Unexpected encoding")

        return base64.b64decode(content).decode("utf-8")
