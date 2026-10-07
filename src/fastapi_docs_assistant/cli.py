import sys

from fastapi_docs_assistant.config import get_settings
from fastapi_docs_assistant.llm import LLMClient
from fastapi_docs_assistant.logging_setup import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    client = LLMClient(
        api_key=settings.openrouter_api_key.get_secret_value(),
        base_url=settings.openrouter_base_url,
        model=settings.llm_model,
    )
    question = " ".join(sys.argv[1:]) or "What is FastAPI?"
    print(client.complete(question).text)
