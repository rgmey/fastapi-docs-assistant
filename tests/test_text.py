import pytest

from fastapi_docs_assistant.text import normalize_whitespace


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("hello   world", "hello world"),
        ("  leading and trailing  ", "leading and trailing"),
        ("line\nbreaks\tand\ttabs", "line breaks and tabs"),
        ("", ""),
    ],
)
def test_normalize_whitespace(raw: str, expected: str) -> None:
    assert normalize_whitespace(raw) == expected
