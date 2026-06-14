import logging
 
import src.config as config
from src.infrastructure import azure_openai_client, stub_openai_client
 
logger = logging.getLogger(__name__)
 
 
def complete(prompt: str, user_content: str) -> dict:
    """Route to stub or real Azure OpenAI client based on USE_STUB_CLIENT config."""
    if config.USE_STUB_CLIENT:
        logger.info("Routing to stub client")
        return stub_openai_client.complete(prompt=prompt, user_content=user_content)
 
    logger.info("Routing to Azure OpenAI client")
    return azure_openai_client.complete(prompt=prompt, user_content=user_content)
