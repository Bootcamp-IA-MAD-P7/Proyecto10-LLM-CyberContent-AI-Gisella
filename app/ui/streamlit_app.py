"""Streamlit interface for the CyberContent AI content generator."""

import streamlit as st

from app.prompts.content_prompt import PLATFORM_RULES
from app.services.brand_profile import BrandProfile
from app.services.content_generator import generate_validated_content

PLATFORM_LABELS: dict[str, str] = {
    "linkedin": "LinkedIn",
    "x": "X (Twitter)",
    "instagram": "Instagram",
    "blog": "Blog",
}


def _split_lines(text: str) -> list[str]:
    """Convert a multi-line text area into a list of non-empty lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def _render_sidebar() -> BrandProfile:
    """Render the brand profile form and return the resulting profile."""
    st.sidebar.header("Brand profile")
    name = st.sidebar.text_input("Brand name", value="CyberContent AI")
    description = st.sidebar.text_area(
        "Description",
        value="Cybersecurity and AI content explained for non-experts.",
    )
    audience = st.sidebar.text_input(
        "Target audience", value="Small business owners"
    )
    language = st.sidebar.selectbox("Language", ["Spanish", "English"])
    goals = st.sidebar.text_area(
        "Content goals (one per line)",
        value="Educate about common threats\nBuild trust",
    )
    guidelines = st.sidebar.text_area(
        "Style guidelines (one per line)",
        value="Clear and friendly tone\nAvoid technical jargon",
    )
    return BrandProfile(
        name=name,
        description=description,
        target_audience=audience,
        content_goals=_split_lines(goals),
        style_guidelines=_split_lines(guidelines),
        language=language,
    )


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="CyberContent AI", layout="wide")
    st.title("CyberContent AI")
    st.write("Generate brand-aligned content for your social networks and blog.")

    profile = _render_sidebar()

    platform = st.selectbox(
        "Platform",
        options=list(PLATFORM_RULES),
        format_func=lambda key: PLATFORM_LABELS[key],
    )
    topic = st.text_input("Topic", placeholder="Example: phishing emails")

    if st.button("Generate content", type="primary"):
        try:
            with st.spinner("Generating content..."):
                result = generate_validated_content(profile, platform, topic)
        except ValueError as error:
            st.error(str(error))
            return
        except Exception as error:
            st.error(f"The content could not be generated: {error}")
            return

        st.subheader("Generated content")
        st.text_area("Result", value=result.content, height=350)

        if result.is_valid:
            st.success(f"Content passed validation (attempts: {result.attempts}).")
        else:
            st.warning("The content did not pass validation:")
            for message in result.errors:
                st.write(f"- {message}")


main()