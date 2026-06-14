import json
import pytest
from unittest.mock import MagicMock

from src.infrastructure import azure_openai_client


def _make_mock_response(content: dict) -> MagicMock:
    """Build a minimal mock mirroring the openai ChatCompletion response shape."""
    mock_message = MagicMock()
    mock_message.content = json.dumps(content)

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    return mock_response


def test_complete_returns_parsed_dict():
    expected = {"summary": "s", "key_points": ["p1"], "risks": []}

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_mock_response(expected)

    result = azure_openai_client.complete(
        prompt="system prompt",
        user_content="document text",
        client=mock_client,
    )

    assert result == expected


def test_complete_sends_correct_message_structure():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_mock_response(
        {"summary": "s", "key_points": ["p"], "risks": []}
    )

    azure_openai_client.complete(
        prompt="my system prompt",
        user_content="my document",
        client=mock_client,
    )

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    messages = call_kwargs["messages"]

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "my system prompt"
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "my document"


def test_complete_enforces_json_mode():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _make_mock_response(
        {"summary": "s", "key_points": ["p"], "risks": []}
    )

    azure_openai_client.complete(
        prompt="prompt",
        user_content="content",
        client=mock_client,
    )

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["response_format"] == {"type": "json_object"}


def test_complete_raises_on_non_json_response():
    mock_message = MagicMock()
    mock_message.content = "This is not JSON"

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])

    with pytest.raises(ValueError, match="not valid JSON"):
        azure_openai_client.complete(
            prompt="prompt",
            user_content="content",
            client=mock_client,
        )