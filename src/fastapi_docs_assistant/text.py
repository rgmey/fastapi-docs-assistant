import re


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace into single spaces and strip the ends."""
    return re.sub(r"\s+", " ", text).strip()
