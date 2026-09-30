import re


def clean_text(text: str) -> str:
    text = text.lower()

    text = re.sub(r"<br\s*/?>", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()