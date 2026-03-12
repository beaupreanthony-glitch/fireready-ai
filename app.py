"""
app.py — FireReady AI
Main Streamlit entry point. Handles page configuration, custom styling,
sidebar navigation, and routing to each module's render() function.
"""

import os
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration — must be the first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="FireReady AI",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS — Deep navy/charcoal theme with red accent
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* =========================================================
       BASE & TYPOGRAPHY
    ========================================================= */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    }

    /* Deep navy main background */
    .main {
        background-color: #07101f;
    }
    .main .block-container {
        background-color: #07101f;
        padding-top: 2rem;
        padding-bottom: 5.5rem; /* room for fixed footer */
    }

    /* Headings — bold and authoritative */
    h1, h2, h3, h4, h5 {
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    }
    h2 {
        font-weight: 800 !important;
        color: #f1f5f9 !important;
        letter-spacing: -0.4px !important;
        border-bottom: 1px solid #1a2744 !important;
        padding-bottom: 0.6rem !important;
        margin-bottom: 1.25rem !important;
    }
    h3 {
        font-weight: 700 !important;
        color: #e2e8f0 !important;
        letter-spacing: -0.3px !important;
    }
    h4 {
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */
    section[data-testid="stSidebar"] {
        background-color: #060d1a;
        border-right: 1px solid #0f1f35;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0;
    }

    /* Nav radio items — bright and readable */
    section[data-testid="stSidebar"] .stRadio label {
        color: #f5f5f5 !important;
        font-size: 1.0rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 0.85rem !important;
        border-radius: 6px !important;
        transition: color 0.15s, background 0.15s !important;
        cursor: pointer !important;
        display: block !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #ffffff !important;
        background: rgba(220, 38, 38, 0.15) !important;
    }
    /* Selected radio item — red highlight */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
        color: #ff4b4b !important;
        background: rgba(220, 38, 38, 0.2) !important;
        font-weight: 800 !important;
    }
    /* Hide default radio circles */
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    /* Hide the nav widget label — combined attribute selector wins specificity battle */
    section[data-testid="stSidebar"] .stRadio > label[data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }

    /* =========================================================
       BUTTONS
    ========================================================= */
    .stButton > button {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.025em !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 2px 12px rgba(185, 28, 28, 0.4) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.55) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 1px 6px rgba(185, 28, 28, 0.3) !important;
    }

    /* Download button — ghost style */
    .stDownloadButton > button {
        background: transparent !important;
        color: #8fafc8 !important;
        border: 1px solid #1a2744 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: #dc2626 !important;
        color: #f87171 !important;
        background: rgba(220, 38, 38, 0.06) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* =========================================================
       FORMS & INPUTS
    ========================================================= */
    [data-testid="stForm"] {
        background: #0b1626 !important;
        border: 1px solid #1a2744 !important;
        border-radius: 12px !important;
        padding: 1.75rem !important;
    }

    /* Input, select, textarea backgrounds */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #0f1e35 !important;
        border-color: #1e3050 !important;
        color: #e2e8f0 !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #dc2626 !important;
        box-shadow: 0 0 0 1px rgba(220, 38, 38, 0.3) !important;
    }

    /* Selectbox */
    [data-baseweb="select"] > div {
        background-color: #0f1e35 !important;
        border-color: #1e3050 !important;
        border-radius: 6px !important;
        color: #e2e8f0 !important;
    }

    /* Slider accent */
    [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
        color: #f87171 !important;
    }
    [data-testid="stSlider"] [role="slider"] {
        background: #dc2626 !important;
    }

    /* =========================================================
       DIVIDERS
    ========================================================= */
    hr {
        border: none !important;
        border-top: 1px solid #1a2744 !important;
        margin: 1.75rem 0 !important;
    }

    /* =========================================================
       ALERTS / CALLOUTS
    ========================================================= */
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"][data-baseweb="notification"] {
        border-radius: 8px !important;
    }
    .stInfo > div {
        background: #060f23 !important;
        border-left-color: #2563eb !important;
    }
    .stWarning > div {
        background: #160b00 !important;
        border-left-color: #d97706 !important;
    }
    .stSuccess > div {
        background: #04120c !important;
        border-left-color: #059669 !important;
    }
    .stError > div {
        background: #130404 !important;
        border-left-color: #dc2626 !important;
    }

    /* =========================================================
       PROGRESS BAR
    ========================================================= */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #dc2626, #f87171) !important;
    }

    /* =========================================================
       EXPANDER
    ========================================================= */
    .streamlit-expanderHeader {
        background: #0b1626 !important;
        border: 1px solid #1a2744 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background: #080f1e !important;
        border: 1px solid #1a2744 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* =========================================================
       BORDERED CONTAINER (used for output cards)
    ========================================================= */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #0b1626 !important;
        border: 1px solid #1a2744 !important;
        border-radius: 12px !important;
    }

    /* =========================================================
       FORM LABELS — all widget labels globally
    ========================================================= */
    label, .stSelectbox label, .stTextInput label, .stTextArea label,
    .stNumberInput label, .stSlider label, .stMultiSelect label,
    .stRadio label, .stCheckbox label,
    [data-testid="stWidgetLabel"] {
        color: #e0e5ed !important;
        font-weight: 500 !important;
    }
    /* Placeholder text */
    ::placeholder { color: #4b6080 !important; opacity: 1 !important; }

    /* =========================================================
       MARKDOWN CONTENT STYLING
    ========================================================= */
    .stMarkdownContainer p {
        color: #d1d5db;
        line-height: 1.75;
    }
    .stMarkdownContainer li {
        color: #d1d5db;
        line-height: 1.75;
    }
    .stMarkdownContainer strong {
        color: #f1f5f9;
        font-weight: 600;
    }
    .stMarkdownContainer a {
        color: #f87171;
    }
    .stMarkdownContainer code {
        background: #1a2e4a !important;
        color: #f87171 !important;
        border-radius: 4px;
        padding: 0.15em 0.4em;
        font-size: 0.88em;
    }

    /* Tables */
    .stMarkdownContainer table {
        border-collapse: collapse;
        width: 100%;
        margin: 0.75rem 0;
    }
    .stMarkdownContainer th {
        background: #122040;
        color: #e2e8f0;
        padding: 0.55rem 0.85rem;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        border: 1px solid #1e3050;
        text-align: left;
    }
    .stMarkdownContainer td {
        color: #c8d4e4;
        padding: 0.5rem 0.85rem;
        border: 1px solid #1a2744;
        font-size: 0.88rem;
        vertical-align: top;
    }
    .stMarkdownContainer tr:nth-child(even) td {
        background: #090f1e;
    }
    .stMarkdownContainer tr:hover td {
        background: rgba(220, 38, 38, 0.04);
    }
    /* Blockquotes */
    .stMarkdownContainer blockquote {
        border-left: 3px solid #dc2626;
        margin-left: 0;
        padding-left: 1rem;
        color: #a0b4cc;
        font-style: italic;
    }

    /* =========================================================
       RADIO BUTTONS (general — non-sidebar)
    ========================================================= */
    .stRadio label { color: #d1d5db !important; }
    .stRadio [data-baseweb="radio"] [data-checked="true"] + label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* =========================================================
       CUSTOM COMPONENT CLASSES
    ========================================================= */

    /* --- Hero (home page) --- */
    .fr-hero {
        background: linear-gradient(140deg, #0b1626 0%, #081020 50%, #0a0f1e 100%);
        border: 1px solid #162038;
        border-radius: 16px;
        padding: 3rem 2.75rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .fr-hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #dc2626 0%, #f87171 50%, transparent 100%);
    }
    .fr-hero::after {
        content: '🔥';
        position: absolute;
        right: 2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 6rem;
        opacity: 0.06;
        line-height: 1;
    }
    .fr-hero-eyebrow {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #dc2626;
        margin-bottom: 0.85rem;
        display: block;
    }
    .fr-hero-title {
        font-size: 3.6rem;
        font-weight: 900;
        color: #f1f5f9;
        letter-spacing: -1.5px;
        line-height: 1.0;
        margin: 0 0 0.9rem 0;
    }
    .fr-hero-title .accent {
        color: #dc2626;
    }
    .fr-hero-sub {
        font-size: 1.1rem;
        color: #b0c4d8;
        line-height: 1.65;
        max-width: 560px;
        margin: 0 0 1.75rem 0;
    }
    .fr-stat-bar {
        display: flex;
        gap: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #162038;
    }
    .fr-stat-num {
        font-size: 1.6rem;
        font-weight: 900;
        color: #f1f5f9;
        display: block;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .fr-stat-label {
        font-size: 0.68rem;
        font-weight: 600;
        color: #c0cad8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: block;
        margin-top: 0.25rem;
    }

    /* --- Disclaimer banner --- */
    .fr-disclaimer {
        background: #0c1220;
        border: 1px solid #1a2744;
        border-left: 3px solid #374151;
        border-radius: 0 8px 8px 0;
        padding: 0.65rem 1.25rem;
        font-size: 0.8rem;
        color: #9aadc4;
        margin-bottom: 1.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* --- Module cards grid --- */
    .fr-cards-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .fr-card {
        background: #0b1626;
        border: 1px solid #162038;
        border-bottom: none;
        border-radius: 12px 12px 0 0;
        padding: 1.6rem 1.4rem 1.4rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }
    .fr-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #dc2626, transparent);
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    .fr-card:hover {
        border-color: #243d5c;
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
    .fr-card:hover::after {
        opacity: 1;
    }

    /* ---- Card launch buttons — fuse to card bottom ---- */
    /* Remove gap between card markdown and button */
    [data-testid="stColumn"]:has(.fr-card) [data-testid="stMarkdownContainer"] {
        margin-bottom: 0 !important;
    }
    [data-testid="stColumn"]:has(.fr-card) [data-testid="stButton"] {
        margin-top: 0 !important;
    }
    /* Style the button as card footer */
    [data-testid="stColumn"]:has(.fr-card) [data-testid="stButton"] button {
        background: #0d1a2e !important;
        border: 1px solid #162038 !important;
        border-top: 1px solid #1e3050 !important;
        border-radius: 0 0 12px 12px !important;
        color: #7bafd4 !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        padding: 0.55rem 1rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    [data-testid="stColumn"]:has(.fr-card) [data-testid="stButton"] button:hover {
        background: rgba(220, 38, 38, 0.14) !important;
        border-color: rgba(220, 38, 38, 0.4) !important;
        border-top-color: rgba(220, 38, 38, 0.4) !important;
        color: #ff6b6b !important;
    }
    .fr-card-icon {
        font-size: 2rem;
        margin-bottom: 0.85rem;
        display: block;
        filter: drop-shadow(0 2px 8px rgba(0,0,0,0.5));
    }
    .fr-card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.2px;
    }
    .fr-card-desc {
        font-size: 0.84rem;
        color: #b8ccde;
        line-height: 1.6;
        margin: 0 0 0.9rem 0;
    }
    .fr-tag {
        display: inline-block;
        background: #0f1e35;
        border: 1px solid #1a2e4a;
        color: #7090b0;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
    }

    /* --- Info row (home page bottom) --- */
    .fr-info-block {
        background: #0b1626;
        border: 1px solid #162038;
        border-radius: 12px;
        padding: 1.5rem;
    }
    .fr-info-block h4 {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #6b8aaa !important;
        margin-bottom: 0.75rem !important;
    }
    .fr-info-block li {
        color: #b8ccde;
        font-size: 0.87rem;
        line-height: 1.7;
    }
    .fr-info-block li strong {
        color: #e0e5ed;
    }

    /* --- Module page header --- */
    .fr-page-header {
        background: linear-gradient(135deg, #0b1a30 0%, #080f1e 100%);
        border: 1px solid #162038;
        border-left: 4px solid #dc2626;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem 2rem;
        margin-bottom: 1.75rem;
        position: relative;
    }
    .fr-page-eyebrow {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #dc2626;
        margin-bottom: 0.4rem;
        display: block;
    }
    .fr-page-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #f1f5f9;
        letter-spacing: -0.5px;
        margin: 0 0 0.45rem 0;
        line-height: 1.1;
    }
    .fr-page-desc {
        font-size: 0.88rem;
        color: #b0c4d8;
        line-height: 1.65;
        margin: 0 0 0.85rem 0;
        max-width: 640px;
    }
    .fr-audience-badge {
        display: inline-block;
        background: rgba(220, 38, 38, 0.15);
        border: 1px solid rgba(220, 38, 38, 0.3);
        color: #f87171;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
    }

    /* --- Output card label --- */
    .fr-output-label {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #dc2626;
        color: #ffffff;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 0.35rem 0.9rem;
        border-radius: 6px 6px 0 0;
        margin-bottom: 0;
    }

    /* --- Sidebar brand --- */
    .fr-sidebar-brand {
        font-size: 1.35rem;
        font-weight: 900;
        color: #f1f5f9;
        letter-spacing: -0.5px;
        display: block;
        line-height: 1.15;
    }
    .fr-sidebar-brand .accent { color: #dc2626; }
    .fr-sidebar-tagline {
        font-size: 0.65rem;
        font-weight: 600;
        color: #1e3050;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        display: block;
        margin-top: 0.2rem;
        padding-bottom: 0.25rem;
    }
    .fr-sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, #dc2626 0%, #1a2744 60%, transparent 100%);
        margin: 0.85rem 0;
    }
    .fr-sidebar-section {
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #aaaaaa;
        margin-bottom: 0.35rem;
        display: block;
    }
    .fr-sidebar-status {
        background: #0b1626;
        border: 1px solid #1a2744;
        border-radius: 8px;
        padding: 0.6rem 0.85rem;
        margin-top: 0.5rem;
    }
    .fr-sidebar-status-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.4rem;
        vertical-align: middle;
    }
    .fr-sidebar-status-text {
        font-size: 0.78rem;
        font-weight: 600;
        vertical-align: middle;
    }
    .fr-sidebar-footer-text {
        font-size: 0.7rem;
        color: #4b6a8a;
        line-height: 1.5;
        margin-top: 0.75rem;
        display: block;
    }

    /* --- Fixed footer --- */
    .fr-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(4, 8, 20, 0.97);
        backdrop-filter: blur(8px);
        border-top: 1px solid #0f1e35;
        padding: 0.55rem 2rem;
        font-size: 0.72rem;
        color: #4b6a8a;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 9999;
    }
    .fr-footer-brand {
        font-weight: 700;
        color: #6b8aaa;
    }
    .fr-footer-brand .accent { color: #9b3030; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Fixed footer — injected once, visible on all pages
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="fr-footer">
        <span class="fr-footer-brand">
            Fire<span class="accent">Ready</span> AI
        </span>
        <span>For training &amp; education use only — Not for emergency response</span>
        <span>Powered by Claude AI &nbsp;·&nbsp; v1.0</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<span class="fr-sidebar-brand">Fire<span class="accent">Ready</span> AI</span>'
        '<span class="fr-sidebar-tagline">Training &amp; Development</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="fr-sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="fr-sidebar-section">Modules</span>', unsafe_allow_html=True)

    page = st.radio(
        "nav",
        [
            "🏠  Home",
            "💪  Fitness Planner",
            "📚  Knowledge & Quiz",
            "📅  Annual Planner",
            "🎯  Scenario Trainer",
            "🛠️  Drill Builder",
            "⭐  Officer Development",
        ],
        key="sidebar_nav",
        label_visibility="hidden",
    )

    st.markdown('<div class="fr-sidebar-divider"></div>', unsafe_allow_html=True)

    # API status indicator
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())
    if api_key_set:
        st.markdown(
            '<div class="fr-sidebar-status">'
            '<span class="fr-sidebar-status-dot" style="background:#059669;box-shadow:0 0 6px #059669;"></span>'
            '<span class="fr-sidebar-status-text" style="color:#34d399;">AI Connected</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="fr-sidebar-status">'
            '<span class="fr-sidebar-status-dot" style="background:#d97706;"></span>'
            '<span class="fr-sidebar-status-text" style="color:#fbbf24;">Demo Mode</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<span class="fr-sidebar-footer-text">'
        'Set ANTHROPIC_API_KEY<br>to enable full AI generation.'
        '</span>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Page routing — strip emoji prefix added for styling
# ---------------------------------------------------------------------------
# Map display labels back to logical page names
_PAGE_MAP = {
    "🏠  Home": "Home",
    "💪  Fitness Planner": "Fitness Planner",
    "📚  Knowledge & Quiz": "Knowledge & Quiz Center",
    "📅  Annual Planner": "Annual Training Planner",
    "🎯  Scenario Trainer": "Scenario Trainer",
    "🛠️  Drill Builder": "Company Drill Builder",
    "⭐  Officer Development": "Officer Development",
}
current_page = _PAGE_MAP.get(page, "Home")

# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
if current_page == "Home":

    # Hero section
    st.markdown(
        """
        <div class="fr-hero">
            <span class="fr-hero-eyebrow">Firefighter Readiness Platform</span>
            <div class="fr-hero-title">Fire<span class="accent">Ready</span> AI</div>
            <div class="fr-hero-sub">
                AI-powered training, planning, and readiness tools built for the fire service.
                From individual fitness to department-wide annual training plans.
            </div>
            <div class="fr-stat-bar">
                <div>
                    <span class="fr-stat-num">6</span>
                    <span class="fr-stat-label">Training Modules</span>
                </div>
                <div>
                    <span class="fr-stat-num">12</span>
                    <span class="fr-stat-label">Knowledge Topics</span>
                </div>
                <div>
                    <span class="fr-stat-num">10</span>
                    <span class="fr-stat-label">Scenario Types</span>
                </div>
                <div>
                    <span class="fr-stat-num">∞</span>
                    <span class="fr-stat-label">AI-Generated Plans</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Disclaimer
    st.markdown(
        '<div class="fr-disclaimer">'
        '⚠️&nbsp;&nbsp;<strong style="color:#6b7280;">Training Tool Only.</strong>'
        '&nbsp;FireReady AI is designed for education, planning, and individual readiness — '
        'not for live incident command or emergency response. Validate all outputs against '
        'your department\'s SOGs and applicable NFPA standards.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Module cards
    modules = [
        {
            "icon": "💪",
            "title": "Fitness Planner",
            "desc": "Personalized weekly PT plans tailored to your role, fitness level, available equipment, and primary goal.",
            "tag": "Individual Firefighters",
            "nav_label": "💪  Fitness Planner",
        },
        {
            "icon": "📚",
            "title": "Knowledge & Quiz Center",
            "desc": "Study guides and scored interactive quizzes across 12 core fire service topics — fire behavior to MAYDAY.",
            "tag": "Study · Quiz Modes",
            "nav_label": "📚  Knowledge & Quiz",
        },
        {
            "icon": "📅",
            "title": "Annual Training Planner",
            "desc": "Full-year Crawl → Walk → Run department training calendar with monthly progressions and a capstone event.",
            "tag": "Training Officers",
            "nav_label": "📅  Annual Planner",
        },
        {
            "icon": "🎯",
            "title": "Scenario Trainer",
            "desc": "Branching fireground scenarios with tactical decision points, consequences, and a structured training debrief.",
            "tag": "Interactive · Decision-Making",
            "nav_label": "🎯  Scenario Trainer",
        },
        {
            "icon": "🛠️",
            "title": "Drill Builder",
            "desc": "Complete drill night plan — objectives, timed timeline, equipment list, safety notes, and evaluation criteria.",
            "tag": "Company Officers",
            "nav_label": "🛠️  Drill Builder",
        },
        {
            "icon": "⭐",
            "title": "Officer Development",
            "desc": "Command checklists, leadership practice prompts, and development questions for aspiring and current officers.",
            "tag": "Career Development",
            "nav_label": "⭐  Officer Development",
        },
    ]

    st.markdown('<div class="fr-cards-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")
    cols = [col1, col2, col3]
    for i, mod in enumerate(modules):
        with cols[i % 3]:
            st.markdown(
                f"""<div class="fr-card">
                    <span class="fr-card-icon">{mod["icon"]}</span>
                    <div class="fr-card-title">{mod["title"]}</div>
                    <div class="fr-card-desc">{mod["desc"]}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(mod["tag"], key=f"card_{i}", use_container_width=True):
                st.session_state.sidebar_nav = mod["nav_label"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Info row
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown(
            '<div class="fr-info-block">'
            '<h4>Getting Started</h4>'
            '<ul style="margin:0;padding-left:1.25rem;">'
            '<li><strong>Click any module card</strong> above, or use the sidebar</li>'
            '<li>Fill in the form and click <strong>Generate</strong></li>'
            '<li>Download any output as a <strong>Markdown file</strong></li>'
            '<li>Set <strong>ANTHROPIC_API_KEY</strong> to enable full AI generation</li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            '<div class="fr-info-block">'
            '<h4>Built For</h4>'
            '<ul style="margin:0;padding-left:1.25rem;">'
            '<li><strong>Firefighters</strong> — fitness plans, study guides, scenario practice</li>'
            '<li><strong>Company Officers</strong> — drill builder, scenarios, officer development</li>'
            '<li><strong>Training Officers</strong> — annual planning and curriculum design</li>'
            '<li><strong>Promotional Candidates</strong> — knowledge quizzes and command prep</li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# MODULE ROUTING
# ---------------------------------------------------------------------------
elif current_page == "Fitness Planner":
    from modules.fitness_planner import render
    render()

elif current_page == "Knowledge & Quiz Center":
    from modules.knowledge_quiz import render
    render()

elif current_page == "Annual Training Planner":
    from modules.annual_planner import render
    render()

elif current_page == "Scenario Trainer":
    from modules.scenario_trainer import render
    render()

elif current_page == "Company Drill Builder":
    from modules.drill_builder import render
    render()

elif current_page == "Officer Development":
    from modules.officer_development import render
    render()
