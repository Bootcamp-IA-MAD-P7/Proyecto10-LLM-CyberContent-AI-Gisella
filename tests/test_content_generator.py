"""Tests for the validated content generation flow."""

import pytest

from app.services import content_generator
from app.services.brand_profile import BrandProfile
from app.services.content_generator import generate_validated_content


@pytest.fixture
def profile() -> BrandProfile:
    return BrandProfile(
        name="CyberShield",
        description="Cybersecurity awareness for small businesses.",
        target_audience="Small business owners.",
    )


def _fake_generator(responses: list[str]):
    """Return a stand-in for generate_content that yields fixed responses."""
    calls = iter(responses)

    def fake(profile, platform, topic):
        return next(calls)

    return fake


def test_valid_content_needs_one_attempt(monkeypatch, profile):
    monkeypatch.setattr(
        content_generator,
        "generate_content",
        _fake_generator(["Use strong passwords. #security"]),
    )
    result = generate_validated_content(profile, "x", "passwords")
    assert result.is_valid
    assert result.attempts == 1


def test_invalid_content_is_retried(monkeypatch, profile):
    monkeypatch.setattr(
        content_generator,
        "generate_content",
        _fake_generator(["a" * 300, "Use strong passwords. #security"]),
    )
    result = generate_validated_content(profile, "x", "passwords")
    assert result.is_valid
    assert result.attempts == 2


def test_content_still_invalid_after_all_attempts(monkeypatch, profile):
    monkeypatch.setattr(
        content_generator,
        "generate_content",
        _fake_generator(["a" * 300, "b" * 300]),
    )
    result = generate_validated_content(profile, "x", "passwords")
    assert not result.is_valid
    assert result.attempts == 2
    assert result.content == "b" * 300