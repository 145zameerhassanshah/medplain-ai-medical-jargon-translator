import streamlit as st

from config import (
    APP_NAME,
    APP_TAGLINE,
    OPENROUTER_API_KEY,
    SUPPORTED_LANGUAGES,
    READING_LEVELS,
)

from prompts import build_system_prompt
from services.llm_service import translate_clinical_note


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "clinical_note" not in st.session_state:
    st.session_state.clinical_note = ""

if "translation" not in st.session_state:
    st.session_state.translation = ""

if "translated_note" not in st.session_state:
    st.session_state.translated_note = ""


# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #E5E7EB;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .app-kicker {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 0.3rem;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 750;
        color: #0F172A;
        margin-bottom: 0.15rem;
    }

    .app-subtitle {
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: #ECFDF5;
        color: #047857;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid #A7F3D0;
    }

    .sidebar-brand {
        font-size: 1.4rem;
        font-weight: 750;
        color: #0F172A;
    }

    .sidebar-caption {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }

    .privacy-note {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.9rem;
        color: #475569;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 12px;
        min-height: 250px;
        font-size: 0.96rem;
        line-height: 1.6;
    }

    div[data-testid="stButton"] button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 42px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    .result-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin-bottom: 0.5rem;
    }

    .footer-note {
        text-align: center;
        color: #94A3B8;
        font-size: 0.78rem;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">🩺 MedPlain AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'Patient-friendly healthcare communication'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")

    st.markdown("**Medical Jargon Translator**")
    st.caption(
        "Convert clinical terminology into clear "
        "patient-friendly language."
    )

    st.divider()

    st.markdown("### Translation Settings")

    selected_language = st.selectbox(
        "Output Language",
        SUPPORTED_LANGUAGES,
        index=0,
    )

    reading_level = st.selectbox(
        "Reading Level",
        READING_LEVELS,
        index=1,
        help=(
            "Simple uses easier wording. "
            "Detailed provides more explanation."
        ),
    )

    st.divider()

    st.markdown("### API Status")

    if OPENROUTER_API_KEY:
        st.success("API configured")
    else:
        st.error("API key missing")

    st.divider()

    st.markdown(
        """
        <div class="privacy-note">
        <strong>Privacy reminder</strong><br><br>
        For this learning version, use synthetic or
        de-identified clinical notes. Avoid entering
        patient names, IDs, addresses, phone numbers,
        or other identifying information.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center",
)

with header_left:

    st.markdown(
        '<div class="app-kicker">AI HEALTH COMMUNICATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-title">Medical Jargon Translator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="app-subtitle">{APP_TAGLINE}</div>',
        unsafe_allow_html=True,
    )


with header_right:

    if OPENROUTER_API_KEY:
        st.markdown(
            '<div class="status-badge">● AI Ready</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------------

with st.container(border=True):

    st.markdown("### Understand clinical notes more easily")

    st.write(
        "Paste a clinical note below. MedPlain AI converts "
        "complex medical terminology into clear, "
        "patient-friendly language while preserving the "
        "original clinical meaning."
    )


st.write("")


# ---------------------------------------------------------
# INPUT SETTINGS
# ---------------------------------------------------------

settings_left, settings_right = st.columns(2)

with settings_left:

    st.markdown("**Output language**")
    st.caption(selected_language)


with settings_right:

    st.markdown("**Explanation level**")
    st.caption(reading_level)


# ---------------------------------------------------------
# CLINICAL NOTE INPUT
# ---------------------------------------------------------

st.markdown("### Clinical Note")

st.caption(
    "Paste the clinical text you want to simplify."
)

clinical_note = st.text_area(
    "Clinical Note Input",
    value=st.session_state.clinical_note,
    height=280,
    placeholder=(
        "Example:\n\n"
        "Pt presents with SOB x 2 days. "
        "CXR demonstrates RLL infiltrate. "
        "BP 150/95 mmHg. "
        "Possible lower respiratory tract infection."
    ),
    label_visibility="collapsed",
)


# ---------------------------------------------------------
# NOTE INFORMATION
# ---------------------------------------------------------

character_count = len(clinical_note)
word_count = len(clinical_note.split())

info_left, info_right = st.columns(2)

with info_left:
    st.caption(f"{word_count} words")

with info_right:
    st.caption(f"{character_count} characters")


# ---------------------------------------------------------
# ACTION BUTTONS
# ---------------------------------------------------------

button_translate, button_example, button_clear, spacer = st.columns(
    [1.5, 1, 1, 4]
)


with button_translate:

    translate_clicked = st.button(
        "✨ Translate Note",
        type="primary",
        use_container_width=True,
    )


with button_example:

    example_clicked = st.button(
        "Use Example",
        use_container_width=True,
    )


with button_clear:

    clear_clicked = st.button(
        "Clear",
        use_container_width=True,
    )


# ---------------------------------------------------------
# EXAMPLE NOTE
# ---------------------------------------------------------

if example_clicked:

    st.session_state.clinical_note = (
        "Pt presents with SOB x 2 days. "
        "CXR shows RLL infiltrate. "
        "BP 150/95 mmHg. "
        "Possible lower respiratory tract infection."
    )

    st.session_state.translation = ""
    st.session_state.translated_note = ""

    st.rerun()


# ---------------------------------------------------------
# CLEAR
# ---------------------------------------------------------

if clear_clicked:

    st.session_state.clinical_note = ""
    st.session_state.translation = ""
    st.session_state.translated_note = ""

    st.rerun()


# ---------------------------------------------------------
# TRANSLATION PROCESS
# ---------------------------------------------------------

if translate_clicked:

    cleaned_note = clinical_note.strip()

    if not cleaned_note:

        st.warning(
            "Please enter a clinical note before translating."
        )

    elif len(cleaned_note) < 10:

        st.warning(
            "The clinical note is too short. "
            "Please provide more clinical information."
        )

    elif not OPENROUTER_API_KEY:

        st.error(
            "The API key is not configured. "
            "Please check the .env file."
        )

    else:

        system_prompt = build_system_prompt(
            selected_language=selected_language,
            reading_level=reading_level,
        )

        with st.spinner(
            "MedPlain AI is preparing a patient-friendly explanation..."
        ):

            translation = translate_clinical_note(
                system_prompt=system_prompt,
                clinical_note=cleaned_note,
            )

        st.session_state.clinical_note = cleaned_note
        st.session_state.translated_note = cleaned_note
        st.session_state.translation = translation


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

if st.session_state.translation:

    st.write("")
    st.divider()

    st.markdown("## Translation Result")

    st.caption(
        f"{selected_language} • {reading_level} explanation"
    )

    original_col, translation_col = st.columns(
        2,
        gap="large",
    )


    # ORIGINAL NOTE
    with original_col:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">'
                'Original Clinical Note'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                st.session_state.translated_note
            )


    # TRANSLATION
    with translation_col:

        with st.container(border=True):

            st.markdown(
                '<div class="result-label">'
                'Patient-Friendly Explanation'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                st.session_state.translation
            )


    st.info(
        "This tool simplifies existing clinical information. "
        "It is not intended to diagnose medical conditions "
        "or replace advice from a qualified healthcare professional."
    )


# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------

else:

    st.write("")

    with st.container(border=True):

        st.markdown("#### Your translation will appear here")

        st.caption(
            "Enter a clinical note and select "
            "Translate Note to generate a plain-language explanation."
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer-note">
    MedPlain AI • Clinical language made clear
    </div>
    """,
    unsafe_allow_html=True,
)