"""
Classical Cryptography Toolkit
================================
Main Streamlit application entry point.
Handles sidebar navigation and page routing.

Run with:
    streamlit run app.py
"""

import streamlit as st
from pathlib import Path

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Classical Cryptography Toolkit",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Classical Cryptography Toolkit — Final Year Network Security Mini Project",
    },
)


# ── Load Custom CSS ───────────────────────────────────────────────────────────
def load_css():
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


load_css()

# ── Import Views ──────────────────────────────────────────────────────────────
from views.home import render as home_render
from views.caesar_page import render as caesar_render
from views.monoalphabetic_page import render as mono_render
from views.playfair_page import render as playfair_render
from views.hill_page import render as hill_render
from views.vigenere_page import render as vigenere_render
from views.otp_page import render as otp_render
from views.rail_fence_page import render as rail_fence_render
from views.columnar_page import render as columnar_render
from views.learn_page import render as learn_render
from views.compare_page import render as compare_render
from views.file_page import render as file_render
from views.help_page import render as help_render
from views.about_page import render as about_render

# ── Navigation Structure ──────────────────────────────────────────────────────
NAV_STRUCTURE = {
    "🏠 Dashboard": {
        "🏠 Home": home_render,
    },
    "🔄 Substitution Ciphers": {
        "Caesar Cipher": caesar_render,
        "Monoalphabetic Cipher": mono_render,
        "Playfair Cipher": playfair_render,
        "Hill Cipher": hill_render,
        "Vigenère Cipher": vigenere_render,
        "One-Time Pad": otp_render,
    },
    "🔀 Transposition Ciphers": {
        "Rail Fence Cipher": rail_fence_render,
        "Columnar Transposition": columnar_render,
    },
    "📚 Learning": {
        "Learn Algorithms": learn_render,
        "Compare Algorithms": compare_render,
    },
    "🛠️ Utilities": {
        "File Encryption": file_render,
        "Help / User Manual": help_render,
        "About Project": about_render,
    },
}

# Icons for nav items
NAV_ICONS = {
    "🏠 Home": "🏠",
    "Caesar Cipher": "🔡",
    "Monoalphabetic Cipher": "🔤",
    "Playfair Cipher": "🔲",
    "Hill Cipher": "🔢",
    "Vigenère Cipher": "🗝️",
    "One-Time Pad": "🛡️",
    "Rail Fence Cipher": "🚂",
    "Columnar Transposition": "📊",
    "Learn Algorithms": "📖",
    "Compare Algorithms": "📊",
    "File Encryption": "📂",
    "Help / User Manual": "❓",
    "About Project": "ℹ️",
}

# ── Query Parameter Sync for Browser Back/Forward ────────────────────────────────
all_page_names = {}
for sec, pgs in NAV_STRUCTURE.items():
    all_page_names.update(pgs)

query_page = st.query_params.get("page")
if query_page and query_page in all_page_names:
    if st.session_state.get("nav_page") != query_page:
        st.session_state["nav_page"] = query_page
elif "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "🏠 Home"

if "nav_history" not in st.session_state:
    st.session_state["nav_history"] = []


def go_to_page(page_name: str, add_history: bool = True):
    current = st.session_state.get("nav_page", "🏠 Home")
    if add_history and current != page_name:
        hist = st.session_state.get("nav_history", [])
        hist.append(current)
        st.session_state["nav_history"] = hist
    st.session_state["nav_page"] = page_name
    st.query_params["page"] = page_name
    st.rerun()


def go_back():
    hist = st.session_state.get("nav_history", [])
    if hist:
        prev = hist.pop()
        st.session_state["nav_history"] = hist
        st.session_state["nav_page"] = prev
        st.query_params["page"] = prev
    else:
        st.session_state["nav_page"] = "🏠 Home"
        st.query_params["page"] = "🏠 Home"
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / Title
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 0.3rem 0;">
        <div style="font-size:1.8rem;">⚔️</div>
        <div style="font-family:'Orbitron',monospace; font-size:0.75rem; font-weight:700;
                    background:linear-gradient(135deg,#00d4ff,#7c3aed);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:0.08em; margin-top:0.2rem;">
            CRYPTO TOOLKIT
        </div>
        <div style="font-size:0.6rem; color:#64748b; letter-spacing:0.1em;
                    text-transform:uppercase; margin-top:0.1rem;">
            Network Security
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e3a5f;margin:0.5rem 0;'>", unsafe_allow_html=True)

    # ── Quick Nav (shown when not on Home) ────────────────────────────────────
    current_page = st.session_state["nav_page"]
    if current_page != "🏠 Home":
        qc1, qc2 = st.columns(2)
        with qc1:
            if st.button("← Back", key="sidebar_back", use_container_width=True,
                         help="Go to previous page"):
                go_back()
        with qc2:
            if st.button("🏠 Home", key="sidebar_home", use_container_width=True,
                         help="Go to Home page"):
                go_to_page("🏠 Home", add_history=False)
        st.markdown("<div style='height:0.1rem;'></div>", unsafe_allow_html=True)

    # Navigation
    for section, pages in NAV_STRUCTURE.items():
        st.markdown(f"""
        <div class="nav-section-label">{section}</div>
        """, unsafe_allow_html=True)

        for page_name in pages:
            icon = NAV_ICONS.get(page_name, "•")
            if st.button(
                f"{icon}  {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
            ):
                go_to_page(page_name)

        st.markdown("<div style='height:0.25rem;'></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1e3a5f;margin:0.3rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;color:#64748b;font-size:0.65rem;padding:0.3rem 0;">
        Classical Cryptography Toolkit<br>
        Final Year Mini Project • 2026-27
    </div>
    """, unsafe_allow_html=True)

# ── Main Content Area ─────────────────────────────────────────────────────────
current_page = st.session_state["nav_page"]

# Top bar navigation on sub-pages
if current_page != "🏠 Home":
    tc1, tc2, tc3 = st.columns([1, 1, 6])
    with tc1:
        if st.button("← Back", key="top_back_btn", use_container_width=True):
            go_back()
    with tc2:
        if st.button("🏠 Home", key="top_home_btn", use_container_width=True):
            go_to_page("🏠 Home", add_history=False)
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

# Find and call the render function for the current page
if current_page in all_page_names:
    try:
        all_page_names[current_page]()
    except Exception as e:
        st.error(f"❌ Error rendering page '{current_page}': {str(e)}")
        import traceback
        with st.expander("🔍 Error Details (for debugging)"):
            st.code(traceback.format_exc())
else:
    # Default to home if page not found
    home_render()
