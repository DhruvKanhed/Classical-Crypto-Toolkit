"""
Monoalphabetic Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.monoalphabetic import encrypt, decrypt, validate_key
from utils.validators import validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box
)
import string


def render():
    render_cipher_header(
        name="Monoalphabetic Cipher",
        cipher_type="Substitution",
        description="Each letter of the alphabet is mapped to a unique different letter using a fixed permutation (substitution key). Every time a letter appears, it is always replaced by the same cipher letter.",
        key_info="26-character substitution alphabet (all 26 letters, each exactly once)",
        security="Low",
        concept="Each plain letter → fixed unique cipher letter via a substitution table",
        icon="🔤",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")

        plaintext = st.text_area(
            "Plaintext", placeholder="Enter text to encrypt…",
            height=100, key="mono_enc_plain"
        )

        key_input = st.text_input(
            "Substitution Key (26 unique letters)",
            placeholder="e.g., QWERTYUIOPASDFGHJKLZXCVBNM",
            key="mono_enc_key",
            help="Enter all 26 letters of the alphabet in a scrambled order. Each letter must appear exactly once.",
            max_chars=26,
        )

        # Show alphabet mapping if key is entered
        if key_input:
            valid, err = validate_key(key_input)
            if valid:
                success_box(f"Valid key: {key_input.upper()}")
                # Mapping display
                plain_row = list(string.ascii_uppercase)
                cipher_row = list(key_input.upper())
                df_map = pd.DataFrame([cipher_row], columns=plain_row, index=["Cipher"])
                st.markdown("**Alphabet → Cipher Mapping:**")
                st.dataframe(df_map, use_container_width=True)
            else:
                error_box(err)

        if st.button("🔒 Encrypt", key="mono_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            ok2, e2 = validate_key(key_input) if key_input else (False, "Key cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = encrypt(plaintext, key_input)
                dec_result = decrypt(result["ciphertext"], key_input)

                render_result_table([
                    ("Algorithm", "Monoalphabetic Cipher"),
                    ("Plaintext", plaintext),
                    ("Key", key_input.upper()),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])
                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "mono_enc_copy")
                with c2:
                    download_result(result["ciphertext"], "mono_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        ciphertext_in = st.text_area(
            "Ciphertext", placeholder="Enter ciphertext to decrypt…",
            height=100, key="mono_dec_cipher"
        )

        key_dec = st.text_input(
            "Substitution Key (same key used for encryption)",
            placeholder="e.g., QWERTYUIOPASDFGHJKLZXCVBNM",
            key="mono_dec_key", max_chars=26
        )

        if st.button("🔓 Decrypt", key="mono_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            ok2, e2 = validate_key(key_dec) if key_dec else (False, "Key cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = decrypt(ciphertext_in, key_dec)
                render_result_table([
                    ("Algorithm", "Monoalphabetic Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Key", key_dec.upper()),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Plaintext", result["plaintext"])
                copy_text_area("Copy Plaintext", result["plaintext"], "mono_dec_copy")
                download_result(result["plaintext"], "mono_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Monoalphabetic Cipher

        ### What is it?
        A monoalphabetic cipher uses a fixed substitution: every occurrence of a given
        plaintext letter maps to exactly the same ciphertext letter throughout the entire message.
        It is a generalization of the Caesar Cipher where the substitution can be any permutation
        of the alphabet (not just a shift).

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Example:</strong><br><br>
            Plain:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z<br>
            Cipher: Q W E R T Y U I O P A S D F G H J K L Z X C V B N M<br><br>
            Plaintext:  <code>HELLO</code><br>
            H → I, E → T, L → S, L → S, O → G<br>
            Ciphertext: <code>ITSSG</code>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Advantages
            - ✅ Simple to implement
            - ✅ 26! ≈ 4×10²⁶ possible keys (much better than Caesar)
            - ✅ Each key is a complete permutation

            ### Required Key
            A permutation of all 26 letters (e.g., QWERTYUIOPASDFGHJKLZXCVBNM).
            """)
        with col2:
            st.markdown("""
            ### Limitations
            - ❌ Vulnerable to **frequency analysis**
            - ❌ Letter frequencies in ciphertext mirror plaintext
            - ❌ Common letter patterns (the, and, ing) reveal structure
            - ❌ With enough ciphertext, can be broken by hand

            ### Common Attacks
            - **Frequency Analysis:** Match most common cipher letters to E, T, A, O…
            - **Pattern Analysis:** Short words and double-letter patterns
            - **Known Plaintext Attack**
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="error-box">🔴 <strong>LOW</strong> — Despite the large key space, '
                    'monoalphabetic ciphers are easily broken by frequency analysis of the ciphertext letters.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        demo_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        demo_plain = "HELLO WORLD"
        result = encrypt(demo_plain, demo_key)
        dec = decrypt(result["ciphertext"], demo_key)

        st.markdown(f"**Plaintext:** `{demo_plain}`  |  **Key:** `{demo_key}`")
        render_result_table([
            ("Algorithm", "Monoalphabetic Cipher"),
            ("Plaintext", demo_plain),
            ("Key", demo_key),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
        ])

        st.markdown("##### Full Alphabet Mapping")
        df_map = pd.DataFrame(
            result["mapping_table"],
            columns=["Plain Letter", "Cipher Letter"]
        ).T
        st.dataframe(df_map, use_container_width=True)

