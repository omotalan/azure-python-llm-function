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
