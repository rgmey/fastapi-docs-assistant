import logging
import time
from dataclasses import dataclass

import openai
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Raised when an LLM call fails after all retries."""


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_s: float


class LLMClient:
    """The only place in the codebase that knows which LLM SDK we use."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout_s: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout_s,
            max_retries=max_retries,
        )
        self.model = model

    def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        start = time.perf_counter()
        try:
            response = self._client.chat.completions.create(model=self.model, messages=messages)
        except openai.APIError as exc:
            logger.error("LLM call failed model=%s error=%s", self.model, exc)
            raise LLMError(f"LLM call failed: {exc}") from exc
        latency = time.perf_counter() - start

        if not response.choices:
            raise LLMError("LLM returned no choices")

        usage = response.usage
        result = LLMResponse(
            text=response.choices[0].message.content or "",
            model=response.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            latency_s=latency,
        )
        logger.info(
            "LLM call model=%s in=%d out=%d latency=%.2fs",
            result.model,
            result.input_tokens,
            result.output_tokens,
            result.latency_s,
        )
        return result
