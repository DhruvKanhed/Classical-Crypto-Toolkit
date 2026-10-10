"""
Vigenère Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.vigenere import encrypt, decrypt
from utils.validators import validate_vigenere_key, validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box
)


def render():
    render_cipher_header(
        name="Vigenère Cipher",
        cipher_type="Substitution",
        description="A polyalphabetic substitution cipher that uses a repeating keyword to apply multiple Caesar shifts. Different letters in the keyword create different shifts for each plaintext letter, defeating simple frequency analysis.",
        key_info="Alphabetic keyword (any length ≥ 1, repeated to match plaintext length)",
        security="Medium",
        concept="C_i = (P_i + K_i) mod 26  |  P_i = (C_i − K_i) mod 26",
        icon="🗝️",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")
        col1, col2 = st.columns([3, 1])
        with col1:
            plaintext = st.text_area(
                "Plaintext", placeholder="Enter text to encrypt…",
                height=100, key="vig_enc_plain"
            )
        with col2:
            keyword = st.text_input(
                "Keyword", placeholder="e.g., LEMON",
                key="vig_enc_kw",
                help="The keyword is repeated to match the length of the plaintext's alphabetic characters."
            )
            if keyword.strip():
                ok, err = validate_vigenere_key(keyword)
                if ok:
                    # Show key preview
                    alpha_count = sum(1 for ch in (plaintext or "") if ch.isalpha())
                    if alpha_count:
                        kw_upper = keyword.upper()
                        repeated = "".join(kw_upper[i % len(kw_upper)] for i in range(min(alpha_count, 20)))
                        st.markdown(f"""
                        <div class="info-box" style="font-size:0.8rem;">
                            Key stream (first {min(alpha_count, 20)} chars):<br>
                            <code>{repeated}{'…' if alpha_count > 20 else ''}</code>
                        </div>
                        """, unsafe_allow_html=True)

        if st.button("🔒 Encrypt", key="vig_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            ok2, e2 = validate_vigenere_key(keyword) if keyword else (False, "Keyword cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = encrypt(plaintext, keyword)
                dec_result = decrypt(result["ciphertext"], keyword)

                render_result_table([
                    ("Algorithm", "Vigenère Cipher"),
                    ("Plaintext", plaintext),
                    ("Keyword", keyword.upper()),
                    ("Key Stream (alpha chars)", result["key_stream"]),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])

                # Char-by-char table
                if result["char_table"]:
                    st.markdown("##### Character-by-Character Encryption Table")
                    df = pd.DataFrame(
                        result["char_table"],
                        columns=["Plain", "Key Letter", "Shift", "Cipher"]
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)

                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "vig_enc_copy")
                with c2:
                    download_result(result["ciphertext"], "vigenere_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        col1, col2 = st.columns([3, 1])
        with col1:
            ciphertext_in = st.text_area(
                "Ciphertext", placeholder="Enter Vigenère ciphertext…",
                height=100, key="vig_dec_cipher"
            )
        with col2:
            keyword_d = st.text_input(
                "Keyword (same as encryption)", placeholder="e.g., LEMON",
                key="vig_dec_kw"
            )

        if st.button("🔓 Decrypt", key="vig_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            ok2, e2 = validate_vigenere_key(keyword_d) if keyword_d else (False, "Keyword cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = decrypt(ciphertext_in, keyword_d)
                render_result_table([
                    ("Algorithm", "Vigenère Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Keyword", keyword_d.upper()),
                    ("Key Stream", result["key_stream"]),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Text", result["plaintext"])

                if result["char_table"]:
                    st.markdown("##### Character-by-Character Decryption Table")
                    df = pd.DataFrame(
                        result["char_table"],
                        columns=["Cipher", "Key Letter", "Shift", "Plain"]
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)

                copy_text_area("Copy Plaintext", result["plaintext"], "vig_dec_copy")
                download_result(result["plaintext"], "vigenere_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Vigenère Cipher

        ### What is it?
        The Vigenère cipher was described by Giovan Battista Bellaso in 1553 but was later
        misattributed to Blaise de Vigenère. For three centuries it was considered unbreakable
        ("le chiffre indéchiffrable"). It uses multiple Caesar shifts determined by a keyword,
        making simple frequency analysis ineffective.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Example: ATTACKATDAWN + LEMON</strong><br><br>
            Plaintext:  A T T A C K A T D A W N<br>
            Key stream: L E M O N L E M O N L E<br>
            Shifts:     11 4 12 14 13 11 4 12 14 13 11 4<br><br>
            A(0)+L(11) = 11 → L<br>
            T(19)+E(4) = 23 → X<br>
            T(19)+M(12) = 5 → F ... etc.<br><br>
            Ciphertext: L X F O P V E F R N H R
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### The Vigenère Square
            The Vigenère table (26×26 grid) shows all possible Caesar shifts.
            Each row corresponds to a keyword letter shift.
            Look up the column (plain letter) in the row (key letter) → cipher letter.

            ### Why It Defeats Frequency Analysis
            Same plaintext letter encrypted with different key letters produces
            different ciphertext letters. This hides the natural English letter frequency.
            """)
        with col2:
            st.markdown("""
            ### Limitations
            - ❌ Vulnerable to **Kasiski test** (finds repeated sequences → key length)
            - ❌ Index of Coincidence can reveal key length
            - ❌ Once key length is known, broken like multiple Caesar ciphers

            ### Common Attacks
            - **Kasiski Examination** — finds repeated ciphertext sequences
            - **Index of Coincidence** — statistical key-length detection
            - **Frequency Analysis** — after determining key length, solve each Caesar
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="warning-box">🟡 <strong>MEDIUM (for classical ciphers)</strong> — '
                    'Resists simple frequency analysis but broken by Kasiski test (1863). '
                    'OTP is the only theoretically secure variant.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Known Test Vector")
        st.markdown("**Plaintext:** `ATTACKATDAWN`  |  **Keyword:** `LEMON`  |  **Expected:** `LXFOPVEFRNHR`")

        result = encrypt("ATTACKATDAWN", "LEMON")
        dec = decrypt(result["ciphertext"], "LEMON")

        render_result_table([
            ("Plaintext", "ATTACKATDAWN"),
            ("Keyword", "LEMON"),
            ("Key Stream", result["key_stream"]),
            ("Ciphertext", result["ciphertext"]),
            ("Expected", "LXFOPVEFRNHR"),
            ("Match", "✅ YES" if result["ciphertext"] == "LXFOPVEFRNHR" else "❌ NO"),
            ("Decrypted", dec["plaintext"]),
        ])

        render_result_box("🔐 Ciphertext", result["ciphertext"])

        st.markdown("##### Full Encryption Table")
        df = pd.DataFrame(
            result["char_table"],
            columns=["Plain", "Key Letter", "Shift", "Cipher"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

