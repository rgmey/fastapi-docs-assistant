from types import SimpleNamespace

from fastapi_docs_assistant.llm import LLMClient


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


def make_client() -> tuple[LLMClient, FakeCompletions]:
    client = LLMClient(api_key="test", base_url="http://localhost", model="fake-model")
    fake = FakeCompletions()
    client._client = SimpleNamespace(chat=SimpleNamespace(completions=fake))
    return client, fake


def test_complete_returns_text_and_usage() -> None:
    client, _ = make_client()
    result = client.complete("hi")
    assert result.text == "hello"
    assert result.input_tokens == 10
    assert result.output_tokens == 2


def test_system_prompt_is_sent_first() -> None:
    client, fake = make_client()
    client.complete("hi", system="be brief")
    messages = fake.calls[0]["messages"]
    assert messages[0] == {"role": "system", "content": "be brief"}
    assert messages[1] == {"role": "user", "content": "hi"}
