from types import SimpleNamespace

import httpx
import openai
import pytest

from fastapi_docs_assistant.llm import LLMClient, LLMError


class FakeCompletions:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            model="fake-model",
            choices=[SimpleNamespace(message=SimpleNamespace(content="hello"))],
            usage=SimpleNamespace(prompt_tokens=10, completion_tokens=2),
        )


def make_client(monkeypatch: pytest.MonkeyPatch) -> tuple[LLMClient, FakeCompletions]:
    client = LLMClient(api_key="test", base_url="http://localhost", model="fake-model")
    fake = FakeCompletions()
    monkeypatch.setattr(client, "_client", SimpleNamespace(chat=SimpleNamespace(completions=fake)))
    return client, fake


def test_complete_returns_text_and_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = make_client(monkeypatch)
    result = client.complete("hi")
    assert result.text == "hello"
    assert result.input_tokens == 10
    assert result.output_tokens == 2


def test_system_prompt_is_sent_first(monkeypatch: pytest.MonkeyPatch) -> None:
    client, fake = make_client(monkeypatch)
    client.complete("hi", system="be brief")
    messages = fake.calls[0]["messages"]
    assert messages[0] == {"role": "system", "content": "be brief"}
    assert messages[1] == {"role": "user", "content": "hi"}


class FailingCompletions:
    def create(self, **kwargs):
        raise openai.APIConnectionError(request=httpx.Request("POST", "http://localhost"))


def test_api_errors_become_llm_errors() -> None:
    client = LLMClient(api_key="test", base_url="http://localhost", model="fake-model")
    client._client = SimpleNamespace(chat=SimpleNamespace(completions=FailingCompletions()))
    with pytest.raises(LLMError):
        client.complete("hi")
