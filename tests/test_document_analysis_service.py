import pytest
from unittest.mock import patch

from src.application import document_analysis_service
from src.domain.exceptions import ValidationException 

VALID_LLM_RESPONSE = {
    "summary": "A concise summary.",
    "key_points": ["Point one", "Point two"],
    "risks": ["Risk one"],
}

def test_analyze_happy_path():
    with patch(
        "src.application.document_analysis_service.openai_gateway.complete",
        return_value=VALID_LLM_RESPONSE,
    ):
        result = document_analysis_service.analyze({"document": "Some document text."})

    assert result["summary"] == "A concise summary."
    assert result["key_points"] == ["Point one", "Point two"]
    assert result["risks"] == ["Risk one"]

def test_analyze_raises_on_missing_document():
    with pytest.raises(ValidationException, match="Missing required field"):
        document_analysis_service.analyze({})

def test_analyze_raises_on_malformed_llm_response():
    with patch(
        "src.application.document_analysis_service.openai_gateway.complete",
        return_value={"unexpected": "shape"},
    ):
        with pytest.raises(ValidationException):
            document_analysis_service.analyze({"document": "Some text."})

def test_analyze_raises_on_llm_failure():
    with patch(
        "src.application.document_analysis_service.openai_gateway.complete",
        side_effect=RuntimeError("LLM call failed"),
    ):
        with pytest.raises(RuntimeError, match="LLM call failed"):
            document_analysis_service.analyze({"document": "Some text."})