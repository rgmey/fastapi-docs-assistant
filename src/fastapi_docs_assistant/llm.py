import logging
import time
from dataclasses import dataclass

from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_s: float


class LLMClient:
    """The only place in the codebase that knows which LLM SDK we use."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        start = time.perf_counter()
        response = self._client.chat.completions.create(model=self.model, messages=messages)
        latency = time.perf_counter() - start

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
