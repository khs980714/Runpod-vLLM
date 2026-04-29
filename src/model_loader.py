from __future__ import annotations

import os

from huggingface_hub import snapshot_download

from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def resolve_model_path(config: Config) -> str:
    """Return a local path or HuggingFace repo ID ready for vLLM."""

    model_type = config.model_type
    model_name = config.model_name

    if model_type == "public":
        return _load_public(model_name)

    if model_type == "gated":
        return _load_gated(model_name, config.hf_token)

    if model_type == "custom":
        return _load_custom(model_name)

    raise ValueError(f"Unknown model_type: {model_type!r}. Must be public | gated | custom")


# ------------------------------------------------------------------
# Internal loaders
# ------------------------------------------------------------------


def _load_public(repo_id: str) -> str:
    """HuggingFace public model — pass repo_id directly to vLLM."""
    logger.info("[public] model=%s", repo_id)
    return repo_id


def _load_gated(repo_id: str, hf_token: str | None) -> str:
    """HuggingFace gated model — authenticate then download snapshot."""
    if not hf_token:
        raise EnvironmentError(
            "HF_TOKEN is required for model_type=gated but was not set."
        )

    logger.info("[gated] downloading model=%s", repo_id)
    local_dir = snapshot_download(
        repo_id=repo_id,
        token=hf_token,
        local_dir=_cache_dir(repo_id),
        local_dir_use_symlinks=False,
        ignore_patterns=["*.msgpack", "*.h5", "flax_model*", "tf_model*"],
    )
    logger.info("[gated] model saved to %s", local_dir)
    return local_dir


def _load_custom(model_path: str) -> str:
    """Locally fine-tuned model stored on the pod's filesystem."""
    if not os.path.isdir(model_path):
        raise FileNotFoundError(
            f"[custom] model directory not found: {model_path!r}"
        )
    logger.info("[custom] model=%s", model_path)
    return model_path


def _cache_dir(repo_id: str) -> str:
    base = os.environ.get("HF_HOME", "/runpod-volume/hub")
    safe_name = repo_id.replace("/", "--")
    return os.path.join(base, safe_name)
