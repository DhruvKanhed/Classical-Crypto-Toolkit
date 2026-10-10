"""
Hill Cipher Page
"""
import streamlit as st
import pandas as pd
import numpy as np
from ciphers.hill import encrypt, decrypt, validate_matrix
from utils.validators import validate_text_not_empty, validate_hill_matrix
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box, warning_box
)


# A few well-known valid Hill Cipher 2×2 matrices
PRESET_MATRICES = {
    "Classic (3,3,2,5)": [3, 3, 2, 5],
    "Example (6,24,1,13)": [6, 24, 1, 13],
    "Simple (1,2,3,5)": [1, 2, 3, 5],
    "Custom": None,
}


def render_key_matrix_input(prefix: str):
    """Render 2×2 matrix input grid and return [a,b,c,d]."""
    st.markdown("**Key Matrix (2×2):**")
    preset = st.selectbox("Use a preset matrix:", list(PRESET_MATRICES.keys()),
                          key=f"{prefix}_preset")

    if PRESET_MATRICES[preset] is not None:
        vals = PRESET_MATRICES[preset]
        a, b, c, d = vals
    else:
        c1, c2 = st.columns(2)
        with c1:
            a = st.number_input("K[0][0]", value=3, step=1, key=f"{prefix}_a")
            c_v = st.number_input("K[1][0]", value=2, step=1, key=f"{prefix}_c")
        with c2:
            b = st.number_input("K[0][1]", value=3, step=1, key=f"{prefix}_b")
            d = st.number_input("K[1][1]", value=5, step=1, key=f"{prefix}_d")
        c_v = int(c_v)
        vals = [int(a), int(b), int(c_v), int(d)]

    if PRESET_MATRICES[preset] is not None:
        vals = [int(x) for x in PRESET_MATRICES[preset]]
    else:
        vals = [int(a), int(b), int(c_v), int(d)]

    # Display matrix visually
    st.markdown(f"""
    <table class="matrix-table"><tbody>
        <tr><td class="matrix-cell">{vals[0]}</td><td class="matrix-cell">{vals[1]}</td></tr>
        <tr><td class="matrix-cell">{vals[2]}</td><td class="matrix-cell">{vals[3]}</td></tr>
    </tbody></table>
    """, unsafe_allow_html=True)

    return vals


def render():
    render_cipher_header(
        name="Hill Cipher",
        cipher_type="Substitution",
        description="A polygraphic substitution cipher based on linear algebra. Uses matrix multiplication modulo 26 to encrypt blocks of letters simultaneously.",
        key_info="2×2 invertible matrix (values 0–25, determinant must be coprime to 26)",
        security="Medium",
        concept="C = (K × P) mod 26  |  P = (K⁻¹ × C) mod 26",
        icon="🔢",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")
        info_box("Non-alphabetic characters are removed. Text is padded with X if the length is odd.")

        col1, col2 = st.columns([2, 1])
        with col1:
            plaintext = st.text_area(
                "Plaintext", placeholder="Enter text to encrypt…",
                height=100, key="hill_enc_plain"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            alpha_count = sum(1 for ch in plaintext if ch.isalpha()) if plaintext else 0
            st.metric("Alpha Characters", alpha_count)

        matrix_vals = render_key_matrix_input("hill_enc")

        if st.button("🔒 Encrypt", key="hill_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            ok2, e2 = validate_hill_matrix(matrix_vals)
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = encrypt(plaintext, matrix_vals)
                dec_result = decrypt(result["ciphertext"], matrix_vals)

                render_result_table([
                    ("Algorithm", "Hill Cipher"),
                    ("Plaintext", plaintext),
                    ("Processed Plaintext", result["processed_plaintext"]),
                    ("Key Matrix", f"[[{matrix_vals[0]},{matrix_vals[1]}],[{matrix_vals[2]},{matrix_vals[3]}]]"),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])

                # Numeric steps table
                if result["numeric_steps"]:
                    st.markdown("##### Matrix Operation Steps")
                    rows = []
                    for step in result["numeric_steps"]:
                        rows.append({
                            "Plain Pair": step["plain_pair"],
                            "P vector": str(step["plain_vec"]),
                            "C = K×P mod 26": str(step["cipher_vec"]),
                            "Cipher Pair": step["cipher_pair"],
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "hill_enc_copy")
                with c2:
                    download_result(result["ciphertext"], "hill_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        ciphertext_in = st.text_area(
            "Ciphertext", placeholder="Enter Hill ciphertext…",
            height=100, key="hill_dec_cipher"
        )
        matrix_vals_d = render_key_matrix_input("hill_dec")

        if st.button("🔓 Decrypt", key="hill_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            ok2, e2 = validate_hill_matrix(matrix_vals_d)
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = decrypt(ciphertext_in, matrix_vals_d)
                render_result_table([
                    ("Algorithm", "Hill Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Key Matrix", f"[[{matrix_vals_d[0]},{matrix_vals_d[1]}],[{matrix_vals_d[2]},{matrix_vals_d[3]}]]"),
                    ("Inverse Matrix", str(result["inverse_matrix"])),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Text", result["plaintext"])
                copy_text_area("Copy Plaintext", result["plaintext"], "hill_dec_copy")
                download_result(result["plaintext"], "hill_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Hill Cipher

        ### What is it?
        Invented by Lester S. Hill in 1929, the Hill Cipher is a polygraphic substitution cipher
        based on linear algebra. It encrypts multiple letters simultaneously using matrix multiplication
        modulo 26.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Encryption with 2×2 matrix:</strong><br><br>
            Key Matrix K = [[3,3],[2,5]]<br><br>
            Plaintext pair: HI → [7, 8]<br><br>
            C = K × P mod 26<br>
            = [[3,3],[2,5]] × [7,8] mod 26<br>
            = [(3×7 + 3×8), (2×7 + 5×8)] mod 26<br>
            = [45, 54] mod 26<br>
            = [19, 2]<br>
            = T, C<br><br>
            So HI → TC
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Formula
            - **Encrypt:** `C = (K × P) mod 26`
            - **Decrypt:** `P = (K⁻¹ × C) mod 26`

            ### Matrix Requirements
            - Must be 2×2 (this implementation)
            - `det(K) mod 26 ≠ 0`
            - `gcd(det(K), 26) = 1`

            ### Advantages
            - ✅ Encrypts multiple letters simultaneously
            - ✅ Diffuses statistical patterns well
            - ✅ Large key space (2×2 matrix values)
            """)
        with col2:
            st.markdown("""
            ### Decryption Process
            1. Compute `det(K) mod 26`
            2. Find modular inverse of det(K) mod 26
            3. Compute adjugate matrix
            4. K⁻¹ = det_inv × adjugate mod 26
            5. Apply: P = K⁻¹ × C mod 26

            ### Limitations
            - ❌ Vulnerable to known-plaintext attacks
            - ❌ Matrix inversion can be complex
            - ❌ Not all matrices are valid keys

            ### Common Attacks
            - **Known Plaintext Attack:** If attacker knows some plaintext-ciphertext pairs,
              they can solve for the key matrix
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="warning-box">🟡 <strong>MEDIUM (for classical ciphers)</strong> — '
                    'Better than simple substitution due to polygraphic nature, but vulnerable to known-plaintext attacks.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        st.markdown("**Plaintext:** `HELP`  |  **Key Matrix:** [[3,3],[2,5]]")
        ex_matrix = [3, 3, 2, 5]
        result = encrypt("HELP", ex_matrix)
        dec = decrypt(result["ciphertext"], ex_matrix)

        render_result_table([
            ("Plaintext", "HELP"),
            ("Key Matrix", "[[3,3],[2,5]]"),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
        ])
        render_result_box("🔐 Ciphertext", result["ciphertext"])

        st.markdown("##### Step-by-step operations:")
        for step in result["numeric_steps"]:
            st.markdown(f"""
            <div class="info-box">
                Pair: <code>{step['plain_pair']}</code> → P = {step['plain_vec']}<br>
                C = K × P mod 26 = {step['cipher_vec']}<br>
                Cipher Pair: <code>{step['cipher_pair']}</code>
            </div>
            """, unsafe_allow_html=True)

