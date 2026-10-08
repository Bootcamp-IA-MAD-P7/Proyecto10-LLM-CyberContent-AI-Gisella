"""Groq LLM client built on LangChain (ADR-001, ADR-002)."""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b"


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> ChatGroq:
    """Return a configured ChatGroq instance."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Check your .env file.")

    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
    )