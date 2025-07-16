# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import route handlers
from actions.list_files import router as list_files_router
from actions.read_file import router as read_file_router
from actions.scan_repo import router as scan_repo_router
from actions.write_file import router as write_file_router

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("Missing GITHUB_TOKEN in environment")

# Initialize FastAPI app
app = FastAPI(
    title="GPT Gateway",
    description="FastAPI middleware to bridge GPTs and GitHub repositories.",
    version="1.0.0"
)

# Enable CORS (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(list_files_router, prefix="/list-files", tags=["Files"])
app.include_router(read_file_router, prefix="/read-file", tags=["Files"])
app.include_router(scan_repo_router, prefix="/scan-repo", tags=["Repository"])
app.include_router(write_file_router, prefix="/write-file", tags=["Files"])

# Health check
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "message": "GPT Gateway is running"}


from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Serve OpenAPI spec
@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi():
    return FileResponse("openapi.yaml", media_type="text/yaml")

# Serve ai-plugin.json from .well-known/
app.mount(
    "/.well-known",
    StaticFiles(directory=".well-known", html=False),
    name="well-known"
)
