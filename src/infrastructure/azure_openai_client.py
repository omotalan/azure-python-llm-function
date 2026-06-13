import json
import logging

from openai import AzureOpenAI

import src.config as config

logger = logging.getLogger(__name__)

# ADR: response_format={"type": "json_object"} enforces structured JSON output at the API
# level, reinforcing prompt-level instructions. This requires a compatible LLM engine
# e.g. gpt-4o or gpt-4-turbo. If the engine doesn't support JSON mode, remove the
# response_format parameter and rely on prompt-level constraints alone.
# Ref: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/json-mode


def _build_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_key=config.AZURE_OPENAI_KEY,
        api_version="2024-02-01",
    )


def complete(
    prompt: str,
    user_content: str,
    client: AzureOpenAI | None = None,
) -> dict:
    """Send a chat completion request and return the parsed JSON response as a dict."""
    if client is None:
        client = _build_client()

    logger.info("Sending completion request to deployment: %s", config.DEPLOYMENT_NAME)

    response = client.chat.completions.create(
        model=config.DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
    )

    raw: str = response.choices[0].message.content
    logger.info("Received response from Azure OpenAI")

    return json.loads(raw)