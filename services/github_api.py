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


def should_include_file(path: str, name: str) -> bool:
    """
    Return True if the given file should be read for full context.

    - functional_spec.md (root)
    - codex_task_tracker.md (root)
    - any .md file in /docs/ (any depth)
    """
    # Normalize path for reliable matching
    norm_path = path.lstrip("/")

    # Root-level .mds (no '/')
    if name.lower() in {"functional_spec.md", "codex_task_tracker.md"} and "/" not in norm_path:
        return True

    # docs/ at any depth, any .md
    if norm_path.lower().startswith("docs/") and name.lower().endswith(".md"):
        return True

    return False


async def get_file_sha(owner: str, repo: str, path: str, branch: str = "main") -> str | None:
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
    If a file is important for GPT context, include its actual content as "content".
    """
    if current_depth > max_depth:
        return []

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
        elif item["type"] == "file" and should_include_file(item["path"], item["name"]):
            try:
                entry["content"] = await read_file_content(owner, repo, item["path"], branch)
            except Exception as e:
                entry["content_error"] = str(e)

        result.append(entry)

    return result


async def read_file_content(owner: str, repo: str, path: str, branch: str = "main") -> str:
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
