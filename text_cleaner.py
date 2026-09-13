import re


def clean_text(text):
    text = text.lower()

    # Keep important characters used in technical skills
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9+#./\- ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()