from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine import VLLMEngine


async def handle_completions(engine: "VLLMEngine", payload: dict) -> dict:
    prompt: str = payload.get("prompt", "")
    if not prompt:
        return {"error": "prompt field is required"}

    sampling_params = engine.build_sampling_params(payload)
    request_id = str(uuid.uuid4())

    text = await engine.generate_full(prompt, request_id, sampling_params)

    return {
        "id": f"cmpl-{request_id}",
        "object": "text_completion",
        "created": int(time.time()),
        "model": engine.config.model_name,
        "choices": [
            {
                "index": 0,
                "text": text,
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(text.split()),
            "total_tokens": len(prompt.split()) + len(text.split()),
        },
    }
