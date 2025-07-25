## 📘 PRODUCT REQUIREMENT DOCUMENT (PRD)

### 🧱 Epic: GPT-Aware Middleware for GitHub Codebase Scanning and Writing

---

### 🎯 Goal

Enable custom GPT agents (e.g., The Architect, The Polyglot) to:

* Autonomously **read, navigate, write to, and scan** a live GitHub repository.
* Fetch files, recursively crawl directory trees, and access raw content.
* Write to branches by updating or creating files.
* Assess system completeness, inconsistencies, missing layers, unused code, etc.
* Generate accurate PRDs, TECH_SPECs, and Codex-ready tasks using real source code as context.

---

### 💡 Why It Matters

Current GPT agents depend on **manual context injection** (copy/paste) or limited summaries. That:

* Causes blind spots and inconsistencies.
* Prevents deep architectural reasoning.
* Adds overhead for the human orchestrator (you).

To act like software engineers, GPTs need a **shared, live source of truth** (the real repo) and the **ability to propose or apply changes** directly.

---

### 🧰 Features (Functional Scope)

| Feature                      | Description                                                | Status      |
| ---------------------------- | ---------------------------------------------------------- | ----------- |
| Recursive File Tree Scan     | Read and list all files under a folder (depth N).          | ✅ Shipped  |
| Read File Contents           | Base64-decode and return raw content of any file.          | ✅ Shipped  |
| Write File Contents          | Update or create a file in a specified branch.             | ✅ Shipped  |
| Plugin Manifest & OpenAPI    | Provides ai-plugin.json and openapi.yaml for GPT Actions   | ✅ Shipped  |
| **Planned: Detect Module Boundaries** | Identify domain modules from paths.                       | 🚧 Planned  |
| **Planned: Track Missing Interfaces** | Compare usecase interfaces to existing implementations.    | 🚧 Planned  |
| **Planned: Scan for Project Health**  | Report dead code, stubs, TODOs, broken layers.             | 🚧 Planned  |
| **Planned: Enable GPT Planning**      | GPTs generate next features/tasks directly from structure. | 🚧 Planned  |

> Features marked **Planned** are for future versions.

---

### 🧑‍💻 Users

| Role              | How They Use It                                                        |
| ----------------- | ---------------------------------------------------------------------- |
| **The Architect** | Loads full backend structure to assess usecase/repo alignment.         |
| **The Polyglot**  | Loads frontend trees and schemas for UI state/data structure planning. |
| **Codex**         | Uses tasks written by GPTs based on real repo data.                    |
| **All GPTs**      | Can propose or commit changes by writing/updating files safely.        |

---

### 🔒 Constraints

* Must use authenticated GitHub API via personal token.
* All writes must target **non-protected branches** (e.g., `gpt-agent/*`).
* Must not expose GitHub PAT to GPTs or frontend.
* Should cache or paginate results to handle large repos.
* Optional: Require commit message templates from GPTs.

---
