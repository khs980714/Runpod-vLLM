from __future__ import annotations

from typing import AsyncIterator

from vllm import AsyncEngineArgs, AsyncLLMEngine
from vllm.sampling_params import SamplingParams

from src.model_loader import resolve_model_path
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VLLMEngine:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._engine: AsyncLLMEngine | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def load(self) -> None:
        if self._engine is not None:
            return

        model_path = resolve_model_path(self.config)
        logger.info("Loading model: %s", model_path)

        engine_args = AsyncEngineArgs(
            model=model_path,
            tensor_parallel_size=self.config.tensor_parallel_size,
            gpu_memory_utilization=self.config.gpu_memory_utilization,
            max_model_len=self.config.max_model_len,
            dtype=self.config.dtype,
            quantization=self.config.quantization or None,
            trust_remote_code=True,
            disable_log_requests=True,
        )

        self._engine = AsyncLLMEngine.from_engine_args(engine_args)
        logger.info("Model loaded successfully")

    # ------------------------------------------------------------------
    # Inference helpers
    # ------------------------------------------------------------------

    @property
    def engine(self) -> AsyncLLMEngine:
        if self._engine is None:
            raise RuntimeError("Engine not loaded. Call load() first.")
        return self._engine

    async def generate(
        self,
        prompt: str,
        request_id: str,
        sampling_params: SamplingParams,
    ) -> AsyncIterator:
        return self.engine.generate(prompt, sampling_params, request_id)

    async def generate_full(
        self,
        prompt: str,
        request_id: str,
        sampling_params: SamplingParams,
    ) -> str:
        final_output = None
        async for output in await self.generate(prompt, request_id, sampling_params):
            final_output = output

        if final_output is None:
            return ""

        return final_output.outputs[0].text

    def build_sampling_params(self, params: dict) -> SamplingParams:
        return SamplingParams(
            temperature=params.get("temperature", 1.0),
            top_p=params.get("top_p", 1.0),
            top_k=params.get("top_k", -1),
            max_tokens=params.get("max_tokens", 512),
            presence_penalty=params.get("presence_penalty", 0.0),
            frequency_penalty=params.get("frequency_penalty", 0.0),
            stop=params.get("stop", None),
            n=params.get("n", 1),
        )
