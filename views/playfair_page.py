"""
Playfair Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.playfair import encrypt, decrypt, generate_matrix, preprocess_plaintext
from utils.validators import validate_playfair_key, validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box
)


def render_matrix(matrix):
    """Render the 5×5 Playfair matrix as HTML."""
    html = '<table class="matrix-table"><tbody>'
    for row in matrix:
        html += "<tr>"
        for cell in row:
            html += f'<td class="matrix-cell">{cell}</td>'
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


def render():
    render_cipher_header(
        name="Playfair Cipher",
        cipher_type="Substitution",
        description="A digraph substitution cipher that encrypts pairs of letters (digraphs) using a 5×5 matrix built from a keyword. I and J are treated as the same letter.",
        key_info="Keyword (any word/phrase) used to build the 5×5 matrix",
        security="Medium",
        concept="Encrypt pairs of letters using 3 rules: same row, same column, or rectangle swap",
        icon="🔲",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")

        col1, col2 = st.columns(2)
        with col1:
            plaintext = st.text_area(
                "Plaintext", placeholder="Enter text to encrypt…",
                height=100, key="pf_enc_plain",
                help="Non-alphabetic characters are removed. J is treated as I."
            )
        with col2:
            keyword = st.text_input(
                "Keyword", placeholder="e.g., SECURITY",
                key="pf_enc_kw",
                help="The keyword builds the 5×5 Playfair matrix. Duplicate letters are removed."
            )

        if keyword.strip():
            ok, err = validate_playfair_key(keyword)
            if ok:
                matrix = generate_matrix(keyword)
                st.markdown("**Generated 5×5 Playfair Matrix:**")
                render_matrix(matrix)
            else:
                error_box(err)

        if st.button("🔒 Encrypt", key="pf_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            ok2, e2 = validate_playfair_key(keyword)
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = encrypt(plaintext, keyword)
                dec_result = decrypt(result["ciphertext"], keyword)

                st.markdown("#### Results")
                render_result_table([
                    ("Algorithm", "Playfair Cipher"),
                    ("Original Plaintext", plaintext),
                    ("Keyword", keyword.upper()),
                    ("Processed Plaintext", result["processed_text"]),
                    ("Digraphs", " | ".join(result["digraphs"])),
                    ("Cipher Digraphs", " | ".join(result["cipher_digraphs"])),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])

                # Digraph table
                st.markdown("##### Digraph Transformation Table")
                pairs = list(zip(result["digraphs"], result["cipher_digraphs"]))
                df = pd.DataFrame(pairs, columns=["Plain Digraph", "Cipher Digraph"])
                st.dataframe(df, use_container_width=True, hide_index=True)

                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "pf_enc_copy")
                with c2:
                    download_result(result["ciphertext"], "playfair_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        info_box("The ciphertext must have been produced by Playfair encryption. "
                 "Use the same keyword that was used for encryption.")

        col1, col2 = st.columns(2)
        with col1:
            ciphertext_in = st.text_area(
                "Ciphertext", placeholder="Enter Playfair ciphertext…",
                height=100, key="pf_dec_cipher"
            )
        with col2:
            keyword_d = st.text_input(
                "Keyword (same as encryption)", placeholder="e.g., SECURITY",
                key="pf_dec_kw"
            )

        if st.button("🔓 Decrypt", key="pf_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            ok2, e2 = validate_playfair_key(keyword_d)
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = decrypt(ciphertext_in, keyword_d)
                render_result_table([
                    ("Algorithm", "Playfair Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Keyword", keyword_d.upper()),
                    ("Digraphs", " | ".join(result["digraphs"])),
                    ("Plain Digraphs", " | ".join(result["plain_digraphs"])),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Text", result["plaintext"])
                info_box("Note: Padding characters (X) used during encryption may appear in the decrypted text. "
                         "They can be removed manually.")
                copy_text_area("Copy Plaintext", result["plaintext"], "pf_dec_copy")
                download_result(result["plaintext"], "playfair_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Playfair Cipher

        ### What is it?
        The Playfair cipher was invented in 1854 by Charles Wheatstone but popularized
        by Lord Playfair. It was the first practical digraph substitution cipher —
        instead of encrypting one letter at a time, it encrypts pairs of letters.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Step 1: Build the 5×5 Matrix</strong><br>
            • Write the keyword (remove duplicates, J→I)<br>
            • Fill remaining cells with unused letters A–Z (excluding J)<br><br>
            <strong>Step 2: Preprocess Plaintext</strong><br>
            • Remove non-alpha, uppercase, J→I<br>
            • Insert X between repeated letters in same pair<br>
            • Pad with X if odd number of letters<br>
            • Split into digraphs (pairs)<br><br>
            <strong>Step 3: Apply Encryption Rules</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### The Three Playfair Rules")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="crypto-card" style="text-align:center;">
                <div style="font-size:1.5rem;">➡️</div>
                <strong>Rule 1: Same Row</strong><br><br>
                If both letters are in the same row,
                shift each one <strong>right</strong> by one position
                (wrap around).
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="crypto-card" style="text-align:center;">
                <div style="font-size:1.5rem;">⬇️</div>
                <strong>Rule 2: Same Column</strong><br><br>
                If both letters are in the same column,
                shift each one <strong>down</strong> by one position
                (wrap around).
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="crypto-card" style="text-align:center;">
                <div style="font-size:1.5rem;">🔄</div>
                <strong>Rule 3: Rectangle</strong><br><br>
                If neither — each letter is replaced by the letter
                in its own row but in the <strong>other letter's column</strong>.
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Advantages
            - ✅ Encrypts digraphs — harder than single-letter substitution
            - ✅ 25-letter frequency analysis more difficult
            - ✅ Used by British forces in WWI and WWII

            ### I/J Convention
            Since the matrix is 5×5 (25 cells), I and J share one cell.
            This is the standard convention. J in plaintext → I in the matrix.
            """)
        with col2:
            st.markdown("""
            ### Limitations
            - ❌ Still vulnerable to digraph frequency analysis
            - ❌ Only 312 possible digraph pairings to analyze
            - ❌ Repeated patterns in long ciphertexts are detectable
            - ❌ Key space limited to ~25! matrix arrangements

            ### Common Attacks
            - **Digraph Frequency Analysis**
            - **Known Plaintext Attack**
            - **Pattern Matching**
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="warning-box">🟡 <strong>MEDIUM (for classical ciphers)</strong> — '
                    'Harder to break than Caesar or simple monoalphabetic, but not suitable for real security.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        kw = "SECURITY"
        pt = "NETWORKSECURITY"
        result = encrypt(pt, kw)
        dec = decrypt(result["ciphertext"], kw)

        st.markdown(f"**Plaintext:** `{pt}`  |  **Keyword:** `{kw}`")
        render_result_table([
            ("Keyword", kw),
            ("Processed Text", result["processed_text"]),
            ("Digraphs", " | ".join(result["digraphs"])),
            ("Cipher Digraphs", " | ".join(result["cipher_digraphs"])),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
        ])
        render_result_box("🔐 Ciphertext", result["ciphertext"])
        st.markdown("**Playfair Matrix for keyword SECURITY:**")
        render_matrix(result["matrix"])

