import os


# No real Azure resources are contacted during tests — the OpenAI client is always mocked.
# These env vars must be set before src.config is imported.
# src.config reads them at module level; missing required vars raise KeyError at import time.
# setdefault preserves real values already in the environment (e.g., from CI env block).
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_KEY", "test-key-placeholder")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT_NAME", "test-deployment")
os.environ.setdefault("DOCUMENT_MAX_LENGTH", "10000")
os.environ.setdefault("USE_STUB_CLIENT", "false")