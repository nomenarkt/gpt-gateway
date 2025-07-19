Here’s an updated `README.md` reflecting your **Linode** deployment, with all `render.com` references removed and a generic deployment section added.
This version also clarifies your actual endpoints and gives practical info for Linode/self-hosting.

---

````markdown
# GPT Gateway

**Bridge GPTs and GitHub Repositories**  
This FastAPI service enables GPT Actions or external agents to **list, read, write**, and **recursively scan** the contents of a GitHub repository using clean OpenAPI definitions and a plugin manifest.

---

## 🌐 Live Endpoint

> **Base URL**: [https://nomena-gpt.xyz](https://nomena-gpt.xyz)

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

- OpenAPI: [`/openapi.yaml`](https://nomena-gpt.xyz/openapi.yaml)
- Plugin Manifest: [`/.well-known/ai-plugin.json`](https://nomena-gpt.xyz/.well-known/ai-plugin.json)

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

Set your token as an environment variable (e.g., in `.env`):

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx
````

---

## 🧪 Running Tests (locally or CI)

We use `pytest` to test API endpoints with FastAPI's built-in `TestClient`.

1. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
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
├── actions/                   # FastAPI route modules
├── services/                  # GitHub API logic
├── .well-known/               # ai-plugin.json for GPT integration
├── openapi.yaml               # OpenAPI schema (GPT Action schema)
├── main.py                    # App entrypoint
└── test_main.py               # API test suite
```

---

## 🛠️ Deployment (Linode, or Any VPS)

1. **Clone this repository:**

   ```bash
   git clone https://github.com/nomenarkt/gpt-gateway.git
   cd gpt-gateway
   ```

2. **Set up environment:**

   * Place your `.env` with `GITHUB_TOKEN` in the root directory.

3. **Start the FastAPI server:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

4. **(Optional) Use `systemd` or Supervisor for production hosting.**

5. **Configure Nginx as a reverse proxy (see `/etc/nginx/sites-available/default`).**

---

## 📫 Contact

For feedback or support, email: [nomenaarison@gmail.com](mailto:nomenaarison@gmail.com)