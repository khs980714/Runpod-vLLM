from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine import VLLMEngine


def _messages_to_prompt(messages: list[dict]) -> str:
    """Minimal chat-template fallback (role: content pairs)."""
    parts: list[str] = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        parts.append(f"{role}: {content}")
    parts.append("assistant:")
    return "\n".join(parts)


async def handle_chat_completions(engine: "VLLMEngine", payload: dict) -> dict:
    messages: list[dict] = payload.get("messages", [])
    if not messages:
        return {"error": "messages field is required"}

    prompt = _messages_to_prompt(messages)
    sampling_params = engine.build_sampling_params(payload)
    request_id = str(uuid.uuid4())

    text = await engine.generate_full(prompt, request_id, sampling_params)

    return {
        "id": f"chatcmpl-{request_id}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": engine.config.model_name,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(text.split()),
            "total_tokens": len(prompt.split()) + len(text.split()),
        },
    }
