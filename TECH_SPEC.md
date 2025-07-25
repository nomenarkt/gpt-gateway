## ⚙️ TECH\_SPEC.md (Updated)

```markdown
## ⚙️ TECHNICAL SPECIFICATION (TECH_SPEC)

### 🏗 Architecture Overview

A custom **FastAPI** middleware acts as a bridge between:

* GPT Agents (via tool calls)
* GitHub’s REST API (via personal token)
* External clients, with OpenAPI/ai-plugin.json for GPT compatibility

Hosted on **Linode** (see README for latest base URL).

---

### 🔌 Endpoints (Backend Middleware API)

| Endpoint          | Method | Description                                                 | Status          |
| ----------------- | ------ | ----------------------------------------------------------- | --------------- |
| `/list-files`     | GET    | List all files in a given GitHub path.                      | ✅ Shipped      |
| `/read-file`      | GET    | Read and decode a single file.                              | ✅ Shipped      |
| `/scan-repo`      | POST   | Recursively fetch structure + basic summaries.              | ✅ Shipped      |
| `/write-file`     | PUT    | Create or update a file in the repo (in a specific branch). | ✅ Shipped      |
| `/find-dead-code` | POST   | Detect unused/incomplete layers. *(Phase 2 – Planned)*      | 🚧 Planned      |

---

### 📁 Folder Structure

```

gpt-gateway/
│
├── main.py                  # FastAPI app entrypoint
├── actions/
│   ├── list\_files.py
│   ├── read\_file.py
│   ├── scan\_repo.py
│   ├── write\_file.py
├── services/
│   ├── github\_api.py        # Low-level GitHub API wrapper
├── .well-known/             # ai-plugin.json for GPT integration
├── openapi.yaml             # OpenAPI schema (GPT Action schema)
├── .env                     # GITHUB\_TOKEN (not in version control)
├── README.md
└── test\_main.py             # API test suite

````

---

### 🔐 Security

* GitHub PAT is stored securely in `.env`, never exposed externally.
* Only specific non-protected branches (e.g., `gpt-agent/*`) can be written to.
* GPTs must supply commit messages and optionally a commit template (enforced by schema).
* Logging can be enabled for all write actions for audit purposes.

---

### 🧪 Testing Strategy

| Component    | Test Type   | Tool                                    |
| ------------ | ----------- | --------------------------------------- |
| `list-files` | Unit        | Pytest                                  |
| `read-file`  | Integration | Test with real GitHub repo              |
| `scan-repo`  | Load test   | Check performance with large trees      |
| `write-file` | Integration | Ensure new files/branches behave        |
| Security     | Manual      | Ensure token and write access is scoped |

---

### 🧠 GPT Integration Strategy

Example tool (OpenAPI) definition:

```json
{
  "name": "write_file",
  "description": "Create or update a file in the GitHub repo",
  "parameters": {
    "owner": "nomenarkt",
    "repo": "lamina",
    "branch": "gpt-agent/user-module",
    "path": "backend/repository/user_repository.go",
    "content": "<base64_encoded_code>",
    "message": "gpt-write: create user repository scaffold"
  }
}
````

Each GPT can:

* Propose PRs by writing to a GPT-managed branch.
* Apply corrections, tests, or stub generation automatically.
* Log or annotate its reasoning via commit messages.

---

### ✅ Deliverables

* [x] `main.py` with FastAPI app and endpoint routing
* [x] Core actions including `/write-file`
* [x] GitHub service module with read/write API integration
* [x] GPT tool schemas with write enforcement
* [x] Example GPT usage for architecture gap-filling

---

> *Phase 2 features like dead code detection will be tracked separately as planned enhancements.*
