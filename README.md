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

Prerequisites: [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)

```bash
cp local.settings.json.example local.settings.json
# Fill in your Azure credentials in local.settings.json
pip install -r requirements.txt
func start
```

---

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

No real Azure resources required — Azure OpenAI is mocked in all tests.