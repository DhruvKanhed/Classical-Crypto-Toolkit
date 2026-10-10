"""
Shared UI helpers used across all cipher pages.
"""
import streamlit as st
import pandas as pd
from utils.timing import format_time


def render_cipher_header(name: str, cipher_type: str, description: str,
                          key_info: str, security: str, concept: str, icon: str = "🔐"):
    """Render the top info block for a cipher page."""
    sec_map = {"Low": "badge-low", "Medium": "badge-medium",
               "High": "badge-high", "High*": "badge-high"}
    cat_map = {"Substitution": "badge-substitution", "Transposition": "badge-transposition"}
    sec_class = sec_map.get(security, "badge-medium")
    cat_class = cat_map.get(cipher_type, "badge-substitution")

    st.markdown(f"""
    <div class="cipher-header">
        <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem;">
            <span style="font-size:2rem;">{icon}</span>
            <div>
                <h1 style="margin:0 !important;">{name}</h1>
                <div style="margin-top:0.3rem;">
                    <span class="badge {cat_class}">{cipher_type}</span>
                    &nbsp;
                    <span class="badge {sec_class}">Security: {security}</span>
                </div>
            </div>
        </div>
        <p style="color:#94a3b8; margin:0.5rem 0 0 0; font-size:0.92rem;">{description}</p>
        <div style="display:flex; gap:2rem; margin-top:0.75rem; flex-wrap:wrap;">
            <div><span style="color:#64748b;font-size:0.78rem;">🔑 KEY</span><br>
                 <span style="color:#e2e8f0;font-size:0.85rem;">{key_info}</span></div>
            <div><span style="color:#64748b;font-size:0.78rem;">💡 CONCEPT</span><br>
                 <span style="color:#e2e8f0;font-size:0.85rem;">{concept}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_result_table(rows: list[tuple[str, str]]):
    """Render a styled result table from (field, value) pairs."""
    html = '<table class="result-table"><thead><tr><th>Parameter</th><th>Value</th></tr></thead><tbody>'
    for field, value in rows:
        html += f"<tr><td>{field}</td><td>{value}</td></tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


def render_result_box(label: str, value: str):
    """Render a highlighted ciphertext/plaintext output box."""
    st.markdown(f"""
    <div style="background:rgba(0,212,255,0.06); border:1px solid rgba(0,212,255,0.2);
                border-radius:8px; padding:1rem 1.25rem; margin:0.5rem 0;">
        <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.4rem;">{label}</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:1.05rem;
                    color:#00d4ff; word-break:break-all;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def download_result(text: str, filename: str = "result.txt"):
    """Render a download button for result text."""
    st.download_button(
        label="⬇️ Download Result",
        data=text.encode("utf-8"),
        file_name=filename,
        mime="text/plain",
        use_container_width=True,
    )


def copy_text_area(label: str, text: str, key: str):
    """Render a read-only text area for easy manual copy."""
    st.text_area(label, value=text, key=key, height=80)


def render_summary_table(algorithm: str, plaintext: str, key_str: str,
                          ciphertext: str, enc_time: float, dec_time: float = None,
                          decrypted: str = None):
    """Build and render a standard summary result table."""
    rows = [
        ("Algorithm", algorithm),
        ("Input Text", plaintext[:60] + ("…" if len(plaintext) > 60 else "")),
        ("Key", key_str[:40] + ("…" if len(key_str) > 40 else "")),
        ("Encrypted Text", ciphertext[:80] + ("…" if len(ciphertext) > 80 else "")),
    ]
    if decrypted is not None:
        rows.append(("Decrypted Text", decrypted[:80] + ("…" if len(decrypted) > 80 else "")))
    rows.append(("Encryption Time", format_time(enc_time)))
    if dec_time is not None:
        rows.append(("Decryption Time", format_time(dec_time)))
    render_result_table(rows)


def info_box(text: str):
    st.markdown(f'<div class="info-box">ℹ️ {text}</div>', unsafe_allow_html=True)


def warning_box(text: str):
    st.markdown(f'<div class="warning-box">⚠️ {text}</div>', unsafe_allow_html=True)


def success_box(text: str):
    st.markdown(f'<div class="success-box">✅ {text}</div>', unsafe_allow_html=True)


def error_box(text: str):
    st.markdown(f'<div class="error-box">❌ {text}</div>', unsafe_allow_html=True)

