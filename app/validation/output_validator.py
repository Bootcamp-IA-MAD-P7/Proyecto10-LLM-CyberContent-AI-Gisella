"""Basic validation of generated content (US-14a)."""

import re
from dataclasses import dataclass, field

from app.prompts.content_prompt import PLATFORM_ALIASES, PLATFORM_RULES

HASHTAG_PATTERN = re.compile(r"#\w+")
MARKDOWN_PATTERN = re.compile(r"\*|^#{1,6}\s", re.MULTILINE)
SENTENCE_ENDINGS = (".", "!", "?", "…", '"', "”", ")", "»")


def _looks_complete(text: str) -> bool:
    """Return True if the text ends like a finished piece of writing."""
    last_token = text.split()[-1]
    return (
        text.endswith(SENTENCE_ENDINGS)
        or HASHTAG_PATTERN.fullmatch(last_token) is not None
    )


# Ranges are wider than the prompt rules because models do not count exactly.
PLATFORM_LIMITS: dict[str, dict[str, int]] = {
    "x": {"max_chars": 280, "max_hashtags": 2},
    "instagram": {
        "min_words": 60,
        "max_words": 200,
        "min_hashtags": 3,
        "max_hashtags": 5,
    },
    "linkedin": {"min_words": 100, "max_words": 250},
    "blog": {"min_words": 400, "max_words": 850},
}


@dataclass
class ValidationResult:
    """Outcome of validating a piece of generated content."""

    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def validate_output(content: str, platform: str) -> ValidationResult:
    """Check that generated content meets the basic rules of its platform."""
    key = platform.strip().lower()
    key = PLATFORM_ALIASES.get(key, key)
    if key not in PLATFORM_RULES:
        supported = ", ".join(PLATFORM_RULES)
        raise ValueError(f"Unsupported platform '{platform}'. Use one of: {supported}.")

    result = ValidationResult()
    text = content.strip()
    if not text:
        result.errors.append("The response is empty.")
        return result

    limits = PLATFORM_LIMITS[key]
    word_count = len(text.split())
    hashtag_count = len(HASHTAG_PATTERN.findall(text))

    if "max_chars" in limits and len(text) > limits["max_chars"]:
        result.errors.append(
            f"Too long: {len(text)} characters (maximum {limits['max_chars']})."
        )
    if "min_words" in limits and word_count < limits["min_words"]:
        result.errors.append(
            f"Too short: {word_count} words (minimum {limits['min_words']})."
        )
    if "max_words" in limits and word_count > limits["max_words"]:
        result.errors.append(
            f"Too long: {word_count} words (maximum {limits['max_words']})."
        )
    if "min_hashtags" in limits and hashtag_count < limits["min_hashtags"]:
        result.errors.append(
            f"Too few hashtags: {hashtag_count} (minimum {limits['min_hashtags']})."
        )
    if "max_hashtags" in limits and hashtag_count > limits["max_hashtags"]:
        result.errors.append(
            f"Too many hashtags: {hashtag_count} (maximum {limits['max_hashtags']})."
        )
    if MARKDOWN_PATTERN.search(text):
        result.errors.append("Contains Markdown formatting (asterisks or headings).")
    if not _looks_complete(text):
        result.errors.append(
            "The text looks cut off: it does not end like a complete sentence."
        )

    return result