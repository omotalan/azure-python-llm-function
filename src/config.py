import os
 
# Config reads all required values at import time.
# Missing env vars raise KeyError immediately — fail-fast at startup is intentional.
# For local development: copy local.settings.json.example → local.settings.json and fill in values.
# For CI and Azure deployment: set as environment variables / repository secrets.
 
AZURE_OPENAI_ENDPOINT: str = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_KEY: str = os.environ["AZURE_OPENAI_KEY"]
DEPLOYMENT_NAME: str = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
DOCUMENT_MAX_LENGTH: int = int(os.environ.get("DOCUMENT_MAX_LENGTH", "10000"))
USE_STUB_CLIENT: bool = os.environ.get("USE_STUB_CLIENT", "false").lower() == "true"
