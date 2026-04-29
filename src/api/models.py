from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.config import Config


def handle_models(config: "Config") -> dict:
    return {
        "object": "list",
        "data": [
            {
                "id": config.model_name,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "vllm-runpod-serverless",
            }
        ],
    }
