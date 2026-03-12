"""
llm_client.py — Shared Claude API wrapper for FireReady AI.

All modules call call_claude() for AI-generated content.
If no API key is set, returns None and the calling module displays sample content.
"""

from __future__ import annotations

import os
import streamlit as st

# Load .env file if present (optional; does not fail if missing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Model to use across all modules
MODEL = "claude-opus-4-6"

# Default system prompt applied to all requests unless overridden
DEFAULT_SYSTEM = (
    "You are a professional fire service training specialist with deep expertise in "
    "firefighter physical readiness, fire behavior, tactics, incident command, and department "
    "training program design. Produce content that sounds like it was written by an experienced "
    "fire service training officer — practical, direct, and grounded in NFPA standards and "
    "IFSTA principles. Avoid generic language. Format outputs with clear markdown headers, "
    "bullet points, and sections."
)


def get_api_key() -> str:
    """Return the Anthropic API key from the environment."""
    return os.environ.get("ANTHROPIC_API_KEY", "").strip()


def is_api_available() -> bool:
    """Return True if an API key is configured."""
    return bool(get_api_key())


def call_claude(
    prompt: str,
    system: str = DEFAULT_SYSTEM,
    max_tokens: int = 2048,
) -> str | None:
    """
    Call the Claude API with the given prompt and system message.

    Returns the response text on success.
    Returns None if no API key is configured.
    Raises an exception (caught by the caller) on API errors.
    """
    api_key = get_api_key()
    if not api_key:
        return None

    import anthropic  # imported here so the app loads even without the package installed

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def show_no_api_key_warning() -> None:
    """Display a standardized warning when no API key is set."""
    st.warning(
        "**API key not found.** Set the `ANTHROPIC_API_KEY` environment variable to enable "
        "AI-generated content. See the README for setup instructions. "
        "Sample content is shown below for demo purposes.",
        icon="⚠️",
    )


def run_with_spinner(prompt: str, system: str = DEFAULT_SYSTEM, max_tokens: int = 2048) -> str | None:
    """
    Call Claude with a loading spinner. Returns response text or None.
    Displays an error message in the UI on failure.
    """
    try:
        with st.spinner("Generating content via Claude AI..."):
            return call_claude(prompt, system=system, max_tokens=max_tokens)
    except Exception as e:
        st.error(f"API error: {e}")
        return None


# ---------------------------------------------------------------------------
# UI helper functions — shared visual components used by all modules
# ---------------------------------------------------------------------------

def module_header(icon: str, title: str, description: str, audience: str) -> None:
    """
    Render a styled module page header with title, description, and audience badge.
    Call once at the top of each module's render() function.
    """
    st.markdown(
        f"""<div class="fr-page-header">
            <span class="fr-page-eyebrow">FireReady AI</span>
            <div class="fr-page-title">{icon} {title}</div>
            <div class="fr-page-desc">{description}</div>
            <span class="fr-audience-badge">{audience}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def output_header(label: str = "Generated Output") -> None:
    """
    Render a styled red label strip that appears as the header of an output card.
    Follow this immediately with st.container(border=True) containing st.markdown(result).
    """
    st.markdown(
        f'<div class="fr-output-label">▸ &nbsp;{label.upper()}</div>',
        unsafe_allow_html=True,
    )
