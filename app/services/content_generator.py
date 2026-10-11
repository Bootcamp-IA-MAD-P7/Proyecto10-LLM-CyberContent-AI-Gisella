"""Content generation service that chains prompt, model and parser."""

from dataclasses import dataclass, field

from langchain_core.output_parsers import StrOutputParser

from app.llm.groq_client import get_llm
from app.prompts.content_prompt import CONTENT_PROMPT, build_prompt_variables
from app.services.brand_profile import BrandProfile
from app.validation.output_validator import validate_output

MAX_ATTEMPTS = 2


@dataclass
class GenerationResult:
    """Generated content together with its validation outcome."""

    content: str
    errors: list[str] = field(default_factory=list)
    attempts: int = 1

    @property
    def is_valid(self) -> bool:
        return not self.errors


def generate_content(profile: BrandProfile, platform: str, topic: str) -> str:
    """Generate brand-aligned content for a platform and topic."""
    variables = build_prompt_variables(profile, platform, topic)
    chain = CONTENT_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke(variables)


def generate_validated_content(
    profile: BrandProfile,
    platform: str,
    topic: str,
    max_attempts: int = MAX_ATTEMPTS,
) -> GenerationResult:
    """Generate content and retry while it fails basic validation."""
    content = ""
    errors: list[str] = []

    for attempt in range(1, max_attempts + 1):
        content = generate_content(profile, platform, topic)
        errors = validate_output(content, platform).errors
        if not errors:
            return GenerationResult(content=content, errors=[], attempts=attempt)

    return GenerationResult(content=content, errors=errors, attempts=max_attempts)