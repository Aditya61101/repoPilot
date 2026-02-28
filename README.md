# DevAssistant

AI-powered developer assistant that can understand GitHub repositories,
analyze issues, and automate code fixes.

---

## 🚀 Features (Current)

- Fetch GitHub repositories
- Fetch repository issues
- Basic backend architecture (Controller → Service → Integration)

---

## 🛠 Tech Stack (Current)

- Java 21
- Spring Boot
- Maven

---

## Quick Start

- Clone the repo and run the Java API service located in `api-service`.

```powershell
git clone https://github.com/YOUR_USERNAME/devassistant.git
cd devassistant/api-service
```

Set your GitHub token (Windows PowerShell):

```powershell
setx GITHUB_TOKEN "your_github_token_here"
```

Build and run the Spring Boot API:

```powershell
mvn clean install
mvn spring-boot:run
```

---

## What this Project Contains

- `api-service/` — Java 21 + Spring Boot backend providing repository and issue APIs.
- `ai-service/` — (planned) Python/FastAPI service for LLM orchestration.
- `frontend/` — (planned) React/Next.js UI to interact with the assistant.

---

## Features (Current)

- Fetch GitHub repositories and repository metadata.
- Fetch and surface repository issues.
- Simple, layered backend structure: Controller → Service → Integration.

---

## Tech Stack

- Java 21
- Spring Boot
- Maven
- GitHub REST API

---

## Configuration

Create a GitHub personal access token and expose it as an environment variable `GITHUB_TOKEN`.

Example scopes: `repo` (or more limited scopes depending on needs).

---

## Running & Usage

Once the `api-service` is running, open `http://localhost:8080` (or the configured port).

Example endpoints (adjust based on the implemented controllers):

- `GET /api/repos/{owner}/{repo}` — fetch repository details
- `GET /api/repos/{owner}/{repo}/issues` — list issues for a repository

Check the controller implementations under `src/main/java/com/devassistant/api/controller` for the exact routes and payloads.

---

## Development Notes

- Follow the existing package structure when adding features: `controller`, `service`, `integration`, `exception`.
- Add unit tests under `src/test/java/com/devassistant/api`.

---

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit PRs for proposed changes.

---

## License & Contact

This repository does not include a license file. Add one (for example, `MIT`) if you want to allow reuse.

Questions or feedback: open an issue or contact the maintainers.
