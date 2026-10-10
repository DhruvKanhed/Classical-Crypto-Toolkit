"""
Compare Algorithms Page
"""
import streamlit as st
import pandas as pd
import time
from ciphers.caesar import encrypt as caesar_enc
from ciphers.monoalphabetic import encrypt as mono_enc
from ciphers.vigenere import encrypt as vig_enc
from ciphers.otp import encrypt as otp_enc, generate_key as otp_gen
from ciphers.rail_fence import encrypt as rf_enc
from ciphers.columnar import encrypt as col_enc
from ciphers.playfair import encrypt as pf_enc
from ciphers.hill import encrypt as hill_enc
from utils.timing import format_time
from views.ui_helpers import info_box, warning_box


COMPARISON_DATA = [
    {
        "Algorithm": "Caesar Cipher",
        "Type": "Substitution",
        "Key Type": "Integer shift (0–25)",
        "Operation": "Single-letter shift",
        "Security": "🔴 Low",
        "Freq. Analysis": "❌ Vulnerable",
        "Complexity": "O(n) — Very Simple",
    },
    {
        "Algorithm": "Monoalphabetic",
        "Type": "Substitution",
        "Key Type": "26-letter permutation",
        "Operation": "Fixed substitution table",
        "Security": "🔴 Low",
        "Freq. Analysis": "❌ Vulnerable",
        "Complexity": "O(n) — Simple",
    },
    {
        "Algorithm": "Playfair Cipher",
        "Type": "Substitution",
        "Key Type": "Keyword → 5×5 matrix",
        "Operation": "Digraph substitution",
        "Security": "🟡 Medium",
        "Freq. Analysis": "⚠️ Partially resistant",
        "Complexity": "O(n) — Moderate",
    },
    {
        "Algorithm": "Hill Cipher",
        "Type": "Substitution",
        "Key Type": "2×2 invertible matrix",
        "Operation": "Matrix multiplication mod 26",
        "Security": "🟡 Medium",
        "Freq. Analysis": "⚠️ Better resistance",
        "Complexity": "O(n·k²) — Moderate",
    },
    {
        "Algorithm": "Vigenère Cipher",
        "Type": "Substitution",
        "Key Type": "Alphabetic keyword",
        "Operation": "Multiple Caesar shifts",
        "Security": "🟡 Medium",
        "Freq. Analysis": "⚠️ Resists simple analysis",
        "Complexity": "O(n) — Simple",
    },
    {
        "Algorithm": "One-Time Pad",
        "Type": "Substitution",
        "Key Type": "Random key ≥ msg length",
        "Operation": "Vernam cipher (mod 26)",
        "Security": "🟢 High*",
        "Freq. Analysis": "✅ Immune (true random)",
        "Complexity": "O(n) — Simple (but impractical)",
    },
    {
        "Algorithm": "Rail Fence Cipher",
        "Type": "Transposition",
        "Key Type": "Number of rails",
        "Operation": "Zigzag rearrangement",
        "Security": "🔴 Low",
        "Freq. Analysis": "⚠️ Frequencies unchanged",
        "Complexity": "O(n) — Very Simple",
    },
    {
        "Algorithm": "Columnar Transposition",
        "Type": "Transposition",
        "Key Type": "Keyword → column order",
        "Operation": "Column-based rearrangement",
        "Security": "🟡 Medium",
        "Freq. Analysis": "⚠️ Frequencies unchanged",
        "Complexity": "O(n·log k) — Moderate",
    },
]


def safe_encrypt(name: str, text: str) -> dict:
    """Run encryption for a named algorithm with default demo keys. Returns result dict."""
    alpha_text = "".join(ch for ch in text if ch.isalpha()).upper()
    if not alpha_text:
        return {"ciphertext": "(no alpha chars)", "time_taken": 0.0}

    try:
        if name == "Caesar Cipher":
            return caesar_enc(text, 3)
        elif name == "Monoalphabetic":
            return mono_enc(text, "QWERTYUIOPASDFGHJKLZXCVBNM")
        elif name == "Playfair Cipher":
            return pf_enc(text, "SECURITY")
        elif name == "Hill Cipher":
            return hill_enc(text, [3, 3, 2, 5])
        elif name == "Vigenère Cipher":
            return vig_enc(text, "LEMON")
        elif name == "One-Time Pad":
            key = otp_gen(text)
            return otp_enc(text, key)
        elif name == "Rail Fence Cipher":
            return rf_enc(text, 3)
        elif name == "Columnar Transposition":
            cols = 5
            rows = max(1, (len(alpha_text) + cols - 1) // cols)
            return col_enc(alpha_text, rows, cols, "43125")
        else:
            return {"ciphertext": "N/A", "time_taken": 0.0}
    except Exception as e:
        return {"ciphertext": f"Error: {str(e)}", "time_taken": 0.0}


DEMO_KEYS = {
    "Caesar Cipher": "Shift = 3",
    "Monoalphabetic": "QWERTYUIOPASDFGHJKLZXCVBNM",
    "Playfair Cipher": "SECURITY",
    "Hill Cipher": "[[3,3],[2,5]]",
    "Vigenère Cipher": "LEMON",
    "One-Time Pad": "Random (generated)",
    "Rail Fence Cipher": "3 rails",
    "Columnar Transposition": "Rows=dynamic, Cols=5, Key=43125",
}


def render():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem 0;">
        <div class="app-title" style="font-size:1.6rem;">📊 Compare Algorithms</div>
        <p style="color:#94a3b8;margin-top:0.5rem;">
            Side-by-side comparison of all 8 classical cryptography algorithms
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_table, tab_interactive = st.tabs(["📋 Comparison Table", "⚡ Interactive Compare"])

    # ── COMPARISON TABLE TAB ──────────────────────────────────────────────────
    with tab_table:
        st.markdown("### Algorithm Comparison Table")
        df = pd.DataFrame(COMPARISON_DATA)
        st.dataframe(df, use_container_width=True, hide_index=True, height=350)

        st.markdown("---")
        st.markdown("### 📈 Key Observations")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="crypto-card">
                <strong>🔄 Substitution Ciphers</strong><br><br>
                Caesar, Monoalphabetic, Playfair, Hill, Vigenère, and OTP all
                replace letters with other letters. The key difference is <em>how</em>
                the substitution is computed and whether it changes per-letter (polyalphabetic)
                or stays fixed (monoalphabetic).
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="crypto-card">
                <strong>🔀 Transposition Ciphers</strong><br><br>
                Rail Fence and Columnar Transposition do NOT change any letters —
                they only rearrange them. This means letter frequencies in ciphertext
                are identical to plaintext, making frequency analysis detect this type.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Execution Time Note:</strong> On small inputs, execution time differences between algorithms
            are negligible and not indicative of real-world cryptographic performance.
            All classical ciphers run in O(n) for practical input sizes.
        </div>
        """, unsafe_allow_html=True)

    # ── INTERACTIVE COMPARE TAB ───────────────────────────────────────────────
    with tab_interactive:
        st.markdown("### ⚡ Interactive Encryption Comparison")
        info_box("Enter a plaintext and select algorithms to compare. Default demo keys are used for each algorithm.")

        compare_text = st.text_area(
            "Plaintext to compare",
            value="NETWORK SECURITY",
            height=80,
            key="compare_text",
            help="Non-alphabetic characters handled per algorithm rules."
        )

        all_algos = [r["Algorithm"] for r in COMPARISON_DATA]
        selected_algos = st.multiselect(
            "Select algorithms to compare:",
            all_algos,
            default=["Caesar Cipher", "Vigenère Cipher", "Hill Cipher", "Rail Fence Cipher"],
            key="compare_algos",
        )

        if st.button("⚡ Run Comparison", key="compare_run", use_container_width=False):
            if not compare_text.strip():
                st.error("Please enter some plaintext.")
            elif not selected_algos:
                st.error("Please select at least one algorithm.")
            else:
                rows = []
                for algo_name in selected_algos:
                    result = safe_encrypt(algo_name, compare_text)
                    rows.append({
                        "Algorithm": algo_name,
                        "Plaintext": compare_text[:30] + "…" if len(compare_text) > 30 else compare_text,
                        "Key Used": DEMO_KEYS.get(algo_name, "N/A"),
                        "Ciphertext": result["ciphertext"][:50] + "…" if len(result.get("ciphertext", "")) > 50 else result.get("ciphertext", "N/A"),
                        "Encryption Time": format_time(result.get("time_taken", 0)),
                        "Status": "✅ Success" if not str(result.get("ciphertext", "")).startswith("Error") else "❌ Error",
                    })

                df_result = pd.DataFrame(rows)
                st.markdown("#### Comparison Results")
                st.dataframe(df_result, use_container_width=True, hide_index=True)

                # Detailed expanded view
                st.markdown("#### Detailed Results")
                for row in rows:
                    with st.expander(f"🔐 {row['Algorithm']} — {row['Status']}"):
                        st.markdown(f"**Key Used:** `{row['Key Used']}`")
                        st.markdown(f"**Ciphertext:**")
                        st.code(row["Ciphertext"])
                        st.markdown(f"**Encryption Time:** {row['Encryption Time']}")

                st.markdown("""
                <div class="warning-box">
                    ⚠️ OTP uses a randomly generated key each time — its ciphertext will differ on every run.
                    All other algorithms use fixed demo keys as shown above.
                </div>
                """, unsafe_allow_html=True)

