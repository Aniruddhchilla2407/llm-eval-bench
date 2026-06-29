import pytest
from unittest.mock import MagicMock, patch
from llm_eval.adapters import get_adapter
from llm_eval.adapters.openai_adapter import OpenAIAdapter
from llm_eval.adapters.anthropic_adapter import AnthropicAdapter


def test_get_adapter_openai():
    adapter = get_adapter("gpt-4o", api_key="fake-key")
    assert isinstance(adapter, OpenAIAdapter)
    assert adapter.model == "gpt-4o"


def test_get_adapter_anthropic():
    adapter = get_adapter("claude-sonnet-4-6", api_key="fake-key")
    assert isinstance(adapter, AnthropicAdapter)


def test_get_adapter_unknown_model():
    with pytest.raises(ValueError, match="Unknown model"):
        get_adapter("unknown-model-xyz")


def test_openai_adapter_complete():
    with patch("llm_eval.adapters.openai_adapter.openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Paris"
        mock_response.usage.total_tokens = 42
        mock_client.chat.completions.create.return_value = mock_response

        adapter = OpenAIAdapter(model="gpt-4o", api_key="fake-key")
        result = adapter.complete("What is the capital of France?")

        assert result["text"] == "Paris"
        assert result["tokens"] == 42
        assert "latency" in result


def test_anthropic_adapter_complete():
    with patch("llm_eval.adapters.anthropic_adapter.anthropic.Anthropic") as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Paris"
        mock_response.usage.input_tokens = 20
        mock_response.usage.output_tokens = 10
        mock_client.messages.create.return_value = mock_response

        adapter = AnthropicAdapter(model="claude-sonnet-4-6", api_key="fake-key")
        result = adapter.complete("What is the capital of France?")

        assert result["text"] == "Paris"
        assert result["tokens"] == 30
        assert "latency" in result