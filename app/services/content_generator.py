"""Content generation service that chains prompt, model and parser."""

from langchain_core.output_parsers import StrOutputParser

from app.llm.groq_client import get_llm
from app.prompts.content_prompt import CONTENT_PROMPT, build_prompt_variables
from app.services.brand_profile import BrandProfile


def generate_content(profile: BrandProfile, platform: str, topic: str) -> str:
    """Generate brand-aligned content for a platform and topic."""
    variables = build_prompt_variables(profile, platform, topic)
    chain = CONTENT_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke(variables)