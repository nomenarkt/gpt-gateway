# GPT Gateway

**Bridge GPTs and GitHub Repositories**  
This FastAPI service enables GPT Actions or external agents to **list, read, write**, and **recursively scan** the contents of a GitHub repository using clean OpenAPI definitions and a plugin manifest.

---

## 🌐 Live Endpoint

> **Base URL**: [https://gpt-gateway-cigu.onrender.com](https://gpt-gateway-cigu.onrender.com)

---

## 🚀 Features

- ✅ List files in a given path
- ✅ Read the raw content of any file
- ✅ Write/update files with commit messages
- ✅ Recursively scan the repo tree
- ✅ Plugin-compatible via `.well-known/ai-plugin.json`
- ✅ Fully documented with OpenAPI (3.1)

---

## 📁 API Reference

- OpenAPI: [`/openapi.yaml`](https://gpt-gateway-cigu.onrender.com/openapi.yaml)
- Plugin Manifest: [`/.well-known/ai-plugin.json`](https://gpt-gateway-cigu.onrender.com/.well-known/ai-plugin.json)

---

## 🔐 GitHub Permissions

To function properly, your GitHub token must have the following scopes:

| GitHub Permission   | Required |
|---------------------|----------|
| `Contents`          | ✅ Yes   |
| `Metadata`          | ✅ Yes   |
| `Issues`            | ✅ Optional (for future extension) |
| `Pull requests`     | ✅ Optional |
| `Discussions`       | ✅ Optional |

Set your token as an environment variable:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx
````

---

## 🧪 Running Tests (locally or CI)

We use `pytest` to test API endpoints with FastAPI's built-in `TestClient`.

1. Install dependencies:

```bash
pip install -r requirements.txt
pip install pytest
```

2. Run tests:

```bash
pytest
```

---

## 📦 Project Structure

```
.
├── actions/                  # FastAPI route modules
├── services/                # GitHub API logic
├── .well-known/             # ai-plugin.json for GPT integration
├── openapi.yaml             # OpenAPI schema (GPT Action schema)
├── main.py                  # App entrypoint
└── test_main.py             # API test suite
```

---

## 🛠️ Deployment (Render)

Configured via `render.yaml`.
Ensure `.well-known/`, `openapi.yaml`, and `main.py` are in the root of your GitHub repo.

---

## 📫 Contact

For feedback or support, email: [nomenaarison@gmail.com](mailto:nomenaarison@gmail.com)
