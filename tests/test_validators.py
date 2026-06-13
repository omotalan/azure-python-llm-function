import pytest

from src.domain.exceptions import ValidationException
from src.domain import validators


def test_validate_request_missing_document():
    with pytest.raises(ValidationException, match="Missing required field"):
        validators.validate_request({})


def test_validate_request_non_string_document():
    with pytest.raises(ValidationException, match="must be a string"):
        validators.validate_request({"document": 123})


def test_validate_request_empty_string():
    with pytest.raises(ValidationException, match="must not be empty"):
        validators.validate_request({"document": ""})


def test_validate_request_whitespace_only():
    with pytest.raises(ValidationException, match="must not be empty"):
        validators.validate_request({"document": "   "})


def test_validate_request_document_too_long():
    with pytest.raises(ValidationException, match="exceeds maximum length"):
        validators.validate_request({"document": "x" * 10001})


def test_validate_request_valid():
    # Should not raise.
    validators.validate_request({"document": "A valid document."})


def test_validate_response_missing_summary():
    with pytest.raises(ValidationException, match="summary"):
        validators.validate_response({"key_points": ["p"], "risks": []})


def test_validate_response_missing_key_points():
    with pytest.raises(ValidationException, match="key_points"):
        validators.validate_response({"summary": "s", "risks": []})


def test_validate_response_missing_risks():
    with pytest.raises(ValidationException, match="risks"):
        validators.validate_response({"summary": "s", "key_points": ["p"]})


def test_validate_response_wrong_type_key_points():
    with pytest.raises(ValidationException, match="key_points"):
        validators.validate_response({
            "summary": "s",
            "key_points": "not a list",
            "risks": [],
        })


def test_validate_response_valid():
    # Should not raise.
    validators.validate_response({
        "summary": "A summary.",
        "key_points": ["Point one"],
        "risks": [],
    })