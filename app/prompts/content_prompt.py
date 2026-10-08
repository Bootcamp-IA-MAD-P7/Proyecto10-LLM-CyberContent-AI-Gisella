"""Prompt templates for brand-aligned content generation."""

from langchain_core.prompts import ChatPromptTemplate

from app.services.brand_profile import BrandProfile

PLATFORM_RULES: dict[str, str] = {
    "blog": (
        "Write a structured article with a title, an introduction, three to "
        "five sections with subheadings, and a conclusion. Target 500 to 700 words."
    ),
    "x": (
        "Write a single post of at most 280 characters. "
        "Use no more than two hashtags."
    ),
    "instagram": (
        "Write an engaging caption of 80 to 150 words. "
        "End with a call to action and three to five hashtags."
    ),
    "linkedin": (
        "Write a professional post of 120 to 200 words with a strong opening "
        "line and a closing question for the audience."
    ),
}

SYSTEM_MESSAGE = """You are a content writer for the brand described below.
Write only in the brand's voice and follow its style guidelines strictly.
Return only the final content, without comments or explanations.

Brand name: {brand_name}
Description: {brand_description}
Target audience: {target_audience}

Content goals:
{content_goals}

Style guidelines:
{style_guidelines}"""

HUMAN_MESSAGE = """Platform: {platform}
Platform rules: {platform_rules}
Topic: {topic}

Write the content now."""

CONTENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_MESSAGE),
        ("human", HUMAN_MESSAGE),
    ]
)


def _to_bullets(items: list[str]) -> str:
    """Format a list of strings as a bulleted block."""
    if not items:
        return "- None specified"
    return "\n".join(f"- {item}" for item in items)


def build_prompt_variables(
    profile: BrandProfile, platform: str, topic: str
) -> dict[str, str]:
    """Map a BrandProfile and a request to the template variables."""
    key = platform.strip().lower()
    if key not in PLATFORM_RULES:
        supported = ", ".join(PLATFORM_RULES)
        raise ValueError(f"Unsupported platform '{platform}'. Use one of: {supported}.")

    return {
        "brand_name": profile.name,
        "brand_description": profile.description,
        "target_audience": profile.target_audience,
        "content_goals": _to_bullets(profile.content_goals),
        "style_guidelines": _to_bullets(profile.style_guidelines),
        "platform": key,
        "platform_rules": PLATFORM_RULES[key],
        "topic": topic,
    }