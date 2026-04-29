"""Tests for model_loader resolution logic."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from src.model_loader import resolve_model_path
from src.utils.config import Config


def _make_config(model_type: str, model_name: str, hf_token: str | None = None):
    cfg = MagicMock(spec=Config)
    cfg.model_type = model_type
    cfg.model_name = model_name
    cfg.hf_token = hf_token
    return cfg


class TestPublicModel:
    def test_returns_repo_id(self):
        cfg = _make_config("public", "facebook/opt-125m")
        result = resolve_model_path(cfg)
        assert result == "facebook/opt-125m"


class TestGatedModel:
    def test_raises_without_token(self):
        cfg = _make_config("gated", "meta-llama/Llama-2-7b-hf", hf_token=None)
        with pytest.raises(EnvironmentError, match="HF_TOKEN"):
            resolve_model_path(cfg)

    def test_calls_snapshot_download(self, tmp_path):
        cfg = _make_config("gated", "meta-llama/Llama-2-7b-hf", hf_token="hf_abc123")
        with patch("src.model_loader.snapshot_download", return_value=str(tmp_path)) as mock_dl:
            result = resolve_model_path(cfg)
        mock_dl.assert_called_once()
        assert result == str(tmp_path)


class TestCustomModel:
    def test_returns_path_when_exists(self, tmp_path):
        cfg = _make_config("custom", str(tmp_path))
        result = resolve_model_path(cfg)
        assert result == str(tmp_path)

    def test_raises_when_path_missing(self):
        cfg = _make_config("custom", "/nonexistent/model/path")
        with pytest.raises(FileNotFoundError, match="model directory not found"):
            resolve_model_path(cfg)


class TestUnknownType:
    def test_raises_value_error(self):
        cfg = _make_config("unknown", "some-model")
        with pytest.raises(ValueError, match="Unknown model_type"):
            resolve_model_path(cfg)
