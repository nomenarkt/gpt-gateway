# test_main.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

OWNER = "nomenarkt"
REPO = "gpt-gateway"
BRANCH = "main"
TEST_PATH = ""  # root of repo

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_files():
    response = client.get(f"/list-files/?owner={OWNER}&repo={REPO}&path={TEST_PATH}&branch={BRANCH}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "files" in data
    assert isinstance(data["files"], list)


def test_scan_repo():
    payload = {
        "owner": OWNER,
        "repo": REPO,
        "path": TEST_PATH,
        "branch": BRANCH,
        "depth": 1
    }
    response = client.post("/scan-repo/", json=payload)
    assert response.status_code == 200
    assert "tree" in response.json()

def test_openapi_yaml():
    response = client.get("/openapi.yaml")
    assert response.status_code == 200
    assert "openapi" in response.text

def test_plugin_manifest():
    response = client.get("/.well-known/ai-plugin.json")
    assert response.status_code == 200
    assert response.json()["name_for_human"] == "GPT Gateway"
