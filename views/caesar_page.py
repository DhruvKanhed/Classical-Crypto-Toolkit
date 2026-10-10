"""
Caesar Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers import caesar_encrypt, caesar_decrypt
from ciphers.caesar import get_all_shifts_table
from utils.validators import validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, warning_box, error_box, success_box
)


def render():
    render_cipher_header(
        name="Caesar Cipher",
        cipher_type="Substitution",
        description="One of the simplest and most widely known encryption techniques. Each letter in the plaintext is shifted a fixed number of positions down the alphabet.",
        key_info="Integer shift value (any integer, applied mod 26)",
        security="Low",
        concept="C = (P + K) mod 26  |  P = (C − K) mod 26",
        icon="🔡",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")
        col1, col2 = st.columns([2, 1])
        with col1:
            plaintext = st.text_area(
                "Plaintext", placeholder="Enter text to encrypt…",
                height=120, key="caesar_enc_plain",
                help="Enter any text. Non-alphabetic characters are preserved as-is."
            )
        with col2:
            shift = st.slider("Shift Key (K)", min_value=0, max_value=25, value=3,
                              key="caesar_enc_shift",
                              help="Number of positions to shift each letter (0–25)")
            st.markdown(f"""
            <div class="info-box" style="margin-top:0.5rem;">
                Key = <strong>{shift}</strong><br>
                A → {chr((0 + shift) % 26 + ord('A'))}<br>
                B → {chr((1 + shift) % 26 + ord('A'))}<br>
                Z → {chr((25 + shift) % 26 + ord('A'))}
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔒 Encrypt", key="caesar_enc_btn", use_container_width=False):
            ok, err = validate_text_not_empty(plaintext, "Plaintext")
            if not ok:
                error_box(err)
            else:
                result = caesar_encrypt(plaintext, shift)
                # Also decrypt to verify
                dec_result = caesar_decrypt(result["ciphertext"], shift)

                st.markdown("#### Results")
                render_result_table([
                    ("Algorithm", "Caesar Cipher"),
                    ("Plaintext", plaintext),
                    ("Shift Key (K)", str(shift)),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])

                render_result_box("🔐 Ciphertext", result["ciphertext"])

                col_a, col_b = st.columns(2)
                with col_a:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "caesar_enc_copy")
                with col_b:
                    download_result(result["ciphertext"], "caesar_encrypted.txt")

                # Character transformation table
                if result["transformation_table"]:
                    st.markdown("##### Character Transformation Table")
                    df = pd.DataFrame(
                        result["transformation_table"],
                        columns=["Plain Character", "Shift (K)", "Cipher Character"]
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        col1, col2 = st.columns([2, 1])
        with col1:
            ciphertext_in = st.text_area(
                "Ciphertext", placeholder="Enter ciphertext to decrypt…",
                height=120, key="caesar_dec_cipher",
            )
        with col2:
            shift_d = st.slider("Shift Key (K)", min_value=0, max_value=25, value=3,
                                key="caesar_dec_shift")

        if st.button("🔓 Decrypt", key="caesar_dec_btn"):
            ok, err = validate_text_not_empty(ciphertext_in, "Ciphertext")
            if not ok:
                error_box(err)
            else:
                result = caesar_decrypt(ciphertext_in, shift_d)
                st.markdown("#### Results")
                render_result_table([
                    ("Algorithm", "Caesar Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Shift Key (K)", str(shift_d)),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Plaintext", result["plaintext"])
                copy_text_area("Copy Plaintext", result["plaintext"], "caesar_dec_copy")
                download_result(result["plaintext"], "caesar_decrypted.txt")

        # Brute force section
        st.markdown("---")
        st.markdown("#### 🔍 Brute-Force All Shifts")
        info_box("Try all 26 possible shift values to find the correct decryption. "
                 "This demonstrates how easily Caesar Cipher can be broken.")
        bf_text = st.text_input("Enter ciphertext to brute-force:", key="caesar_bf_input")
        if st.button("Try All 26 Shifts", key="caesar_bf_btn"):
            if bf_text.strip():
                results = get_all_shifts_table(bf_text)
                df = pd.DataFrame(results, columns=["Shift (K)", "Decrypted Text"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                error_box("Please enter ciphertext to brute-force.")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Caesar Cipher

        ### What is it?
        The Caesar Cipher is one of the earliest and simplest encryption techniques,
        named after Julius Caesar who reportedly used it in his private correspondence.
        It shifts every letter in the plaintext by a fixed number of positions in the alphabet.

        ### Cipher Type
        **Substitution Cipher** — each letter is replaced by another letter.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Step-by-step Encryption:</strong><br><br>
            1. Write out the plaintext: <code>HELLO</code><br>
            2. Choose a shift key: <code>K = 3</code><br>
            3. For each letter, find its position (A=0, B=1, …, Z=25)<br>
            4. Add the shift: <code>(position + K) mod 26</code><br>
            5. Convert back to a letter<br><br>
            H(7) + 3 = 10 → K<br>
            E(4) + 3 = 7  → H<br>
            L(11) + 3 = 14 → O<br>
            L(11) + 3 = 14 → O<br>
            O(14) + 3 = 17 → R<br><br>
            Result: <code>HELLO → KHOOR</code>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Formula
            - **Encrypt:** `C = (P + K) mod 26`
            - **Decrypt:** `P = (C - K) mod 26`

            Where:
            - `P` = plaintext letter index (A=0…Z=25)
            - `C` = ciphertext letter index
            - `K` = shift key

            ### Required Key
            A single integer from 0 to 25.
            With K=13, the cipher becomes **ROT13**.
            """)
        with col2:
            st.markdown("""
            ### Advantages
            - ✅ Simple to understand and implement
            - ✅ Fast encryption/decryption
            - ✅ Good for teaching cryptography basics

            ### Limitations
            - ❌ Only 25 possible keys (trivial to brute-force)
            - ❌ Vulnerable to frequency analysis
            - ❌ Does not hide letter frequencies
            - ❌ No security for modern use

            ### Common Attacks
            - **Brute Force:** Try all 25 shifts (takes seconds)
            - **Frequency Analysis:** Match letter frequency to English
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="error-box">🔴 <strong>LOW</strong> — Caesar Cipher provides no meaningful security. '
                    'Any child with pen and paper can break it by trying all 25 possible shifts.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        st.markdown("**Plaintext:** `NETWORK SECURITY`  |  **Key:** `5`")

        result_ex = caesar_encrypt("NETWORK SECURITY", 5)
        dec_ex = caesar_decrypt(result_ex["ciphertext"], 5)

        render_result_table([
            ("Algorithm", "Caesar Cipher"),
            ("Plaintext", "NETWORK SECURITY"),
            ("Shift Key", "5"),
            ("Ciphertext", result_ex["ciphertext"]),
            ("Decrypted", dec_ex["plaintext"]),
            ("Encryption Time", format_time(result_ex["time_taken"])),
        ])

        render_result_box("🔐 Result", result_ex["ciphertext"])

        st.markdown("##### Character-by-Character Transformation")
        df = pd.DataFrame(
            result_ex["transformation_table"],
            columns=["Plain", "Shift", "Cipher"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("##### Known Test Vectors")
        vectors = [
            ("HELLO", 3, "KHOOR"),
            ("ABC", 1, "BCD"),
            ("XYZ", 3, "ABC"),
            ("PYTHON", 13, "CLGUBA"),
            ("ATTACKATDAWN", 13, "NGGNPXNGQNJA"),
        ]
        df_vec = pd.DataFrame(vectors, columns=["Plaintext", "Key (K)", "Expected Ciphertext"])
        st.dataframe(df_vec, use_container_width=True, hide_index=True)

