"""Tests for the content prompt template."""

import pytest

from app.prompts.content_prompt import CONTENT_PROMPT, build_prompt_variables
from app.services.brand_profile import BrandProfile


@pytest.fixture
def profile() -> BrandProfile:
    return BrandProfile(
        name="CyberShield",
        description="Cybersecurity awareness for small businesses.",
        target_audience="Small business owners without technical background.",
        content_goals=["Educate about common threats", "Build trust"],
        style_guidelines=["Clear and friendly tone", "Avoid technical jargon"],
    )


def test_prompt_contains_brand_data(profile):
    variables = build_prompt_variables(profile, "linkedin", "phishing awareness")
    messages = CONTENT_PROMPT.format_messages(**variables)

    assert "CyberShield" in messages[0].content
    assert "- Avoid technical jargon" in messages[0].content
    assert "phishing awareness" in messages[1].content


def test_platform_is_case_insensitive(profile):
    variables = build_prompt_variables(profile, " LinkedIn ", "passwords")
    assert variables["platform"] == "linkedin"


def test_unsupported_platform_raises(profile):
    with pytest.raises(ValueError):
        build_prompt_variables(profile, "tiktok", "passwords")