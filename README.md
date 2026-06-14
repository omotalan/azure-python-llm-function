# azure-python-llm-function

A Python microservice built on Azure Functions and Azure OpenAI. Demonstrates the architecture of an LLM-backed HTTP endpoint: structured outputs, layered validation, and deployment scaffolding.

> **Portfolio project.** Goal: demonstrate understanding of Azure AI microservice shape — not production readiness.

---

## Architecture

```
HTTP POST /api/analyze-document
         │
         ▼
function_app.py                            ← Azure Function: HTTP entry point
         │
         ▼
application/document_analysis_service.py  ← Orchestration: validate → call LLM → validate
         │
         ▼
infrastructure/azure_openai_client.py     ← Azure OpenAI call, JSON mode enforced
         │
         ▼
JSON Response
```

| Layer | Module | Responsibility |
|---|---|---|
| Entry point | `function_app.py` | HTTP routing, request/response serialization |
| Application | `application/document_analysis_service.py` | Workflow orchestration, prompt |
| Domain | `domain/validators.py`, `exceptions.py` | Validation rules, error types |
| Infrastructure | `infrastructure/azure_openai_client.py` | Azure OpenAI API integration |

---

## Endpoint

```
POST /api/analyze-document
```

**Request**
```json
{ "document": "Your document text here." }
```

**Response**
```json
{
  "summary": "...",
  "key_points": ["...", "..."],
  "risks": ["..."]
}
```

---

## Local Development

Prerequisites: 
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- Active Virtual environment
  - Create venv `python3 -m venv .venv`
  - Activate venv `source .venv/bin/activate`
- Emulate Azure Storage via Docker: `docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite`

Local Azure host start
```bash
cp local.settings.json.example local.settings.json
# Fill in your Azure credentials in local.settings.json
pip install -r requirements.txt
func start
```

Example cURL API request, for local testing:
```bash
curl -X POST http://localhost:7071/api/analyze-document   -H "Content-Type: application/json"   -d '{"document": "This is a test document."}'
```


---

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

No real Azure resources required — Azure OpenAI is mocked in all tests.

---

## CI/CD

GitHub Actions runs tests on every push and PR. The deploy job is scaffolded but requires Azure credentials to activate. See `.github/workflows/deploy.yml`.

### Commit structure

Commits follow the Domain-Driven Development (DDD) and Test-Driven Development (TDD) based separation of concerns, emulating a simplified, production-grade Jira project. Here I keep commits linked to Epic-level items (multiple commits per Epic, with a summarized description); in a full production-grade project, these Epics would be broken down into Stories/Tasks and subtasks, and each commit would track a single work item.

The Epics are structured as follows:
- AZPY-1: Set up basic architecture and admin files
- AZPY-2: Set up preliminary unit tests (TDD)
- AZPY-3: Design Domain layer
- AZPY-4: Design Application layer
- AZPY-5: Design Infrastructure layer

Every commit is prefixed by the Epic ticket to which it belongs.

---

## Design Notes

- **JSON mode enforced at API level** via `response_format: {"type": "json_object"}`, complementing prompt instructions. Requires gspecific gpt models; see ADR comment in `azure_openai_client.py`.
- **Dual validation**: request payload and LLM response are validated independently.
- **No DDD overhead**: light separation of concerns — no repositories, aggregates, or domain events.
- **Fail-fast config**: missing env vars raise `KeyError` at startup, not mid-request.
