import re

BLOCKED_PHRASES = [
    r"hire me",
    r"dm me",
    r"my clients",
    r"freelance",
    r"consulting",
    r"side work",
    r"rates",
    r"book a call",
    r"available for work",
    r"work with me"
]

def violates_safety(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(phrase, text_lower) for phrase in BLOCKED_PHRASES)

