def reverse(text: str) -> str:
    return text[::-1]


def is_palindrome(text: str) -> bool:
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def word_count(text: str) -> int:
    if not text or not text.strip():
        return 0
    return len(text.split())


def capitalize_words(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())
