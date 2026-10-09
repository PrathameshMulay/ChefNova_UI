import io
import re
from copy import deepcopy

import pandas as pd
import streamlit as st

try:
    import speech_recognition as sr
except ImportError:
    sr = None


st.set_page_config(page_title="ChefNova", page_icon="🍳", layout="wide")

# ---------- Visual system ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
    background: linear-gradient(rgba(248,246,241,.91),rgba(248,246,241,.95)),
                url("https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=2200&q=85");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #202020;
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,.94);
    border-right: 1px solid #e3ded5;
    backdrop-filter: blur(12px);
}
[data-testid="stHeader"] { background: rgba(248,246,241,.75); }
[data-testid="stAppViewContainer"] { background: transparent; }

/* Keep Streamlit text inputs readable on Streamlit Cloud / dark-theme clients */
[data-testid="stTextArea"] label,
[data-testid="stTextInput"] label,
[data-testid="stChatInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label {
    color: #111111 !important;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input,
[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    border: 1px solid #d8d2c8 !important;
    border-radius: 10px !important;
}

[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: #888888 !important;
    -webkit-text-fill-color: #888888 !important;
    opacity: 1 !important;
}

/* Keep dropdowns dark as designed, while their labels remain black */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #292833 !important;
    color: #ffffff !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #ffffff !important;
}
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }

.brand { padding: 0 8px 24px; }
.brand-title { font-size: 25px; font-weight: 700; color: #171717; }
.brand-sub { font-size: 12px; color: #777; margin-top: 3px; }

.page-title { font-size: 31px; font-weight: 700; color: #171717; margin-bottom: 3px; letter-spacing: -.02em; }
.hero-accent { display: inline-block; width: 42px; height: 4px; border-radius: 20px; background: #c9794b; margin-bottom: 12px; }
.page-subtitle { color: #777; font-size: 14px; margin-bottom: 22px; }
.section-title { font-size: 19px; font-weight: 650; color: #202020; margin: 5px 0 13px; }

.card, .chat-card {
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(224,219,209,.95);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 30px rgba(74,62,45,.07);
    backdrop-filter: blur(7px);
}

.recipe-card {
    background: rgba(255,255,255,.96);
