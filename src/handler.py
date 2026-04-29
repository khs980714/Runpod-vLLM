import runpod

from src.engine import VLLMEngine
from src.api.chat import handle_chat_completions
from src.api.completions import handle_completions
from src.api.models import handle_models
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

config = Config()
engine = VLLMEngine(config)


async def handler(job: dict) -> dict:
    job_input: dict = job.get("input", {})
    endpoint: str = job_input.get("endpoint", "chat/completions")

    logger.info("Job received | id=%s endpoint=%s", job.get("id"), endpoint)

    if endpoint in ("chat/completions", "v1/chat/completions"):
        return await handle_chat_completions(engine, job_input)

    if endpoint in ("completions", "v1/completions"):
        return await handle_completions(engine, job_input)

    if endpoint in ("models", "v1/models"):
        return handle_models(config)

    return {"error": f"Unknown endpoint: {endpoint}"}


if __name__ == "__main__":
    logger.info("Starting vLLM RunPod serverless worker")
    engine.load()
    runpod.serverless.start({"handler": handler})
