# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
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

# Resolve base directory
BASE_DIR = Path(__file__).resolve().parent

# Verify required static directory
WELL_KNOWN_DIR = BASE_DIR / ".well-known"
if not WELL_KNOWN_DIR.is_dir():
    raise RuntimeError("Missing `.well-known` directory required for plugin manifest")

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

# Logging middleware (optional for debugging)
@app.middleware("http")
async def log_all_requests(request: Request, call_next):
    print(f"🛰 {request.method} {request.url}")
    return await call_next(request)

# Register routes
app.include_router(list_files_router, prefix="/list-files", tags=["Files"])
app.include_router(read_file_router, prefix="/read-file", tags=["Files"])
app.include_router(scan_repo_router, prefix="/scan-repo", tags=["Repository"])
app.include_router(write_file_router, prefix="/write-file", tags=["Files"])

# Health check
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "message": "GPT Gateway is running"}

# HEAD request for root (required by OpenAI)
@app.head("/", include_in_schema=False)
def head_root():
    return JSONResponse(content=None, status_code=200)

# Serve OpenAPI spec
@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi():
    return FileResponse(BASE_DIR / "openapi.yaml", media_type="text/yaml")

# Serve ai-plugin.json from .well-known/
app.mount(
    "/.well-known",
    StaticFiles(directory=WELL_KNOWN_DIR, html=False),
    name="well-known"
)
