from __future__ import annotations

import os


class Config:
    """Centralised configuration loaded from environment variables."""

    # ── Model identity ────────────────────────────────────────────────
    model_type: str          # public | gated | custom
    model_name: str          # HF repo-id or local path

    # ── HuggingFace auth ─────────────────────────────────────────────
    hf_token: str | None

    # ── vLLM engine settings ──────────────────────────────────────────
    tensor_parallel_size: int
    gpu_memory_utilization: float
    max_model_len: int
    dtype: str
    quantization: str

    def __init__(self) -> None:
        self.model_type = os.environ.get("MODEL_TYPE", "public").lower()
        self.model_name = os.environ.get("MODEL_NAME", "")
        self.hf_token = os.environ.get("HF_TOKEN") or None

        self.tensor_parallel_size = int(os.environ.get("TENSOR_PARALLEL_SIZE", "1"))
        self.gpu_memory_utilization = float(
            os.environ.get("GPU_MEMORY_UTILIZATION", "0.90")
        )
        self.max_model_len = int(os.environ.get("MAX_MODEL_LEN", "4096"))
        self.dtype = os.environ.get("DTYPE", "auto")
        self.quantization = os.environ.get("QUANTIZATION", "")

        self._validate()

    def _validate(self) -> None:
        valid_types = {"public", "gated", "custom"}
        if self.model_type not in valid_types:
            raise ValueError(
                f"MODEL_TYPE must be one of {valid_types}, got {self.model_type!r}"
            )
        if not self.model_name:
            raise ValueError(
                "MODEL_NAME environment variable is required. "
                "Set it in RunPod Template > Environment Variables."
            )
