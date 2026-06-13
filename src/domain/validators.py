import src.config as config
from src.domain.exceptions import ValidationException


def validate_request(payload: dict) -> None:
    if "document" not in payload:
        raise ValidationException("Missing required field: 'document'")

    document = payload["document"]

    if not isinstance(document, str):
        raise ValidationException("Field 'document' must be a string")

    if not document.strip():
        raise ValidationException("Field 'document' must not be empty")

    if len(document) > config.DOCUMENT_MAX_LENGTH:
        raise ValidationException(
            f"Field 'document' exceeds maximum length of {config.DOCUMENT_MAX_LENGTH} characters"
        )


def validate_response(response: dict) -> None:
    required_fields: dict[str, type] = {
        "summary": str,
        "key_points": list,
        "risks": list,
    }

    for field, expected_type in required_fields.items():
        if field not in response:
            raise ValidationException(f"LLM response missing required field: '{field}'")

        if not isinstance(response[field], expected_type):
            raise ValidationException(
                f"LLM response field '{field}' must be {expected_type.__name__}, "
                f"got {type(response[field]).__name__}"
            )
