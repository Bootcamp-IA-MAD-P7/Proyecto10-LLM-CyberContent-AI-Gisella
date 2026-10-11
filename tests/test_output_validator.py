"""Tests for the basic output validator."""

import pytest

from app.validation.output_validator import validate_output


def test_empty_response_is_invalid():
    result = validate_output("   ", "linkedin")
    assert not result.is_valid
    assert "empty" in result.errors[0]


def test_x_post_within_limits_is_valid():
    result = validate_output("Use strong passwords. #security", "x")
    assert result.is_valid


def test_x_post_over_280_characters_is_invalid():
    result = validate_output("a" * 281, "x")
    assert not result.is_valid


def test_x_post_with_too_many_hashtags_is_invalid():
    result = validate_output("Stay safe #one #two #three", "twitter")
    assert not result.is_valid


def test_linkedin_post_too_short_is_invalid():
    result = validate_output("Too short to be a real post.", "linkedin")
    assert not result.is_valid


def test_instagram_needs_minimum_hashtags():
    text = " ".join(["word"] * 80) + " #one"
    result = validate_output(text, "instagram")
    assert not result.is_valid


def test_instagram_caption_within_limits_is_valid():
    text = " ".join(["word"] * 80) + " #one #two #three"
    result = validate_output(text, "instagram")
    assert result.is_valid


def test_unsupported_platform_raises():
    with pytest.raises(ValueError):
        validate_output("Hello", "tiktok")