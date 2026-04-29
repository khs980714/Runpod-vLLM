"""Tests for the RunPod handler routing logic."""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.utils.config import Config


@pytest.fixture()
def config():
    with patch.dict(
        "os.environ",
        {"MODEL_TYPE": "public", "MODEL_NAME": "facebook/opt-125m"},
    ):
        return Config()


@pytest.fixture()
def mock_engine(config):
    engine = MagicMock()
    engine.config = config
    engine.build_sampling_params = MagicMock(return_value=MagicMock())
    engine.generate_full = AsyncMock(return_value="Hello, world!")
    return engine


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestHandlerRouting:
    def test_chat_completions_route(self, mock_engine):
        from src.api.chat import handle_chat_completions

        payload = {
            "endpoint": "chat/completions",
            "messages": [{"role": "user", "content": "Hi"}],
        }
        result = run(handle_chat_completions(mock_engine, payload))
        assert result["object"] == "chat.completion"
        assert result["choices"][0]["message"]["role"] == "assistant"

    def test_completions_route(self, mock_engine):
        from src.api.completions import handle_completions

        payload = {
            "endpoint": "completions",
            "prompt": "Once upon a time",
        }
        result = run(handle_completions(mock_engine, payload))
        assert result["object"] == "text_completion"
        assert "text" in result["choices"][0]

    def test_models_route(self, config):
        from src.api.models import handle_models

        result = handle_models(config)
        assert result["object"] == "list"
        assert result["data"][0]["id"] == config.model_name

    def test_missing_messages_returns_error(self, mock_engine):
        from src.api.chat import handle_chat_completions

        result = run(handle_chat_completions(mock_engine, {}))
        assert "error" in result

    def test_missing_prompt_returns_error(self, mock_engine):
        from src.api.completions import handle_completions

        result = run(handle_completions(mock_engine, {}))
        assert "error" in result
