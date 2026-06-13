import logging

from src.domain import validators
from src.infrastructure import azure_openai_client

logger = logging.getLogger(__name__)

# Prompt is treated as business workflow configuration, not a standalone subsystem. Structure, constraints, and output contract matter more than phrasing

ANALYSIS_PROMPT = """You are a document analysis assistant.

Analyze the document provided by the user and return a single JSON object with exactly
these three fields:

{
  "summary": "<concise summary of the document, 2-4 sentences>",
  "key_points": ["<key point>", ...],
  "risks": ["<risk or concern>", ...]
}

Rules:
- Return only the JSON object. No preamble, no markdown fencing.
- Do not invent facts not present in the document.
- key_points must contain at least one item.
- If no risks are identified, return an empty array for risks.
"""


def analyze(payload: dict) -> dict:
    """Validate the request, call Azure OpenAI, validate and return the structured result."""
    logger.info("Starting document analysis")

    validators.validate_request(payload)

    result = azure_openai_client.complete(
        prompt=ANALYSIS_PROMPT,
        user_content=payload["document"],
    )

    logger.info("LLM response received, validating output structure")
    validators.validate_response(result)

    logger.info("Document analysis complete")
    return result
