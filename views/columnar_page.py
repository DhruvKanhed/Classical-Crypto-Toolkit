"""
Columnar Transposition Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.columnar import encrypt, decrypt
from utils.validators import validate_columnar_params, validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box
)


def render_column_grid(grid: list[list[str]], key_str: str, column_order: list[int]):
    """Render the plaintext grid with key header."""
    n_cols = len(key_str)
    
    html = '<div style="overflow-x:auto;"><table style="border-collapse:separate;border-spacing:3px;">'
    # Key header
    html += "<thead><tr>"
    html += '<th style="color:#64748b;font-size:0.72rem;padding:2px 4px;"></th>'
    for ch in key_str.upper():
        html += f'<th style="background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.4);border-radius:4px;color:#a78bfa;width:36px;height:36px;text-align:center;font-family:monospace;font-size:0.9rem;">{ch}</th>'
    html += "</tr>"
    # Order row
    html += "<tr>"
    html += '<td style="color:#64748b;font-size:0.72rem;text-align:right;padding-right:4px;">Order</td>'
    for col_idx in range(n_cols):
        rank = column_order.index(col_idx) + 1
        html += f'<td style="background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.2);border-radius:4px;color:#00d4ff;width:36px;height:24px;text-align:center;font-family:monospace;font-size:0.78rem;">{rank}</td>'
    html += "</tr></thead>"

    # Data rows
    html += "<tbody>"
    for r_idx, row in enumerate(grid):
        html += "<tr>"
        html += f'<td style="color:#64748b;font-size:0.72rem;text-align:right;padding-right:4px;">R{r_idx}</td>'
        for cell in row:
            is_pad = (cell == 'X')
            bg = "rgba(245,158,11,0.1)" if is_pad else "rgba(14,21,38,0.6)"
            border_col = "rgba(245,158,11,0.3)" if is_pad else "rgba(30,58,95,0.6)"
            html += f'<td style="background:{bg};border:1px solid {border_col};border-radius:4px;color:#e2e8f0;width:36px;height:36px;text-align:center;font-family:monospace;font-size:0.9rem;">{cell if cell else " "}</td>'
        html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


def render():
    render_cipher_header(
        name="Columnar Transposition Cipher",
        cipher_type="Transposition",
        description="A transposition cipher that arranges plaintext in a grid of specified rows and columns, then reads the columns in order determined by the key.",
        key_info="Numeric key (length must equal the number of columns)",
        security="Medium",
        concept="Write row-by-row into grid → read columns in key-determined sorted order",
        icon="📊",
    )

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")
        info_box("Plaintext is placed in a grid of size rows × columns. "
                 "The grid is padded with 'X' up to rows * columns. "
                 "Columns are read according to the sorted order of the numeric key.")

        plaintext = st.text_area(
            "Plaintext", placeholder="Enter text to encrypt…",
            height=100, key="col_enc_plain"
        )
        
        c1, c2, c3 = st.columns(3)
        with c1:
            rows = st.number_input("Number of Rows", min_value=1, max_value=100, value=4, key="col_enc_rows")
        with c2:
            cols = st.number_input("Number of Columns", min_value=1, max_value=100, value=5, key="col_enc_cols")
        with c3:
            key_val = st.text_input("Key (Numeric, length must equal columns)", placeholder="e.g., 43125", key="col_enc_key")

        # Live grid preview
        if plaintext.strip() and key_val.strip():
            ok, err = validate_columnar_params(plaintext, int(rows), int(cols), key_val, "encrypt")
            if ok:
                preview = encrypt(plaintext, int(rows), int(cols), key_val)
                st.markdown("**Column Grid (before encryption):**")
                render_column_grid(preview["grid"], key_val, preview["column_order"])
                st.markdown(f"_Padding character 'X' shown in amber. Column reading order shown in teal._")
            else:
                error_box(err)

        if st.button("🔒 Encrypt", key="col_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            if not ok1:
                error_box(e1)
            else:
                ok2, e2 = validate_columnar_params(plaintext, int(rows), int(cols), key_val, "encrypt")
                if not ok2:
                    error_box(e2)
                else:
                    result = encrypt(plaintext, int(rows), int(cols), key_val)
                    dec_result = decrypt(result["ciphertext"], int(rows), int(cols), key_val)

                    render_result_table([
                        ("Algorithm", "Columnar Transposition"),
                        ("Plaintext", plaintext),
                        ("Key", key_val),
                        ("Padded Text", result["padded_text"]),
                        ("Grid Size", f"{result['num_rows']} rows × {result['num_cols']} cols"),
                        ("Column Reading Order (0-indexed)", str(result["column_order"])),
                        ("Ciphertext", result["ciphertext"]),
                        ("Verified Decrypt", dec_result["plaintext"]),
                        ("Encryption Time", format_time(result["time_taken"])),
                    ])
                    render_result_box("🔐 Ciphertext", result["ciphertext"])

                    co1, co2 = st.columns(2)
                    with co1:
                        copy_text_area("Copy Ciphertext", result["ciphertext"], "col_enc_copy")
                    with co2:
                        download_result(result["ciphertext"], "columnar_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        info_box("Enter the ciphertext, number of columns, and the same key used during encryption. "
                 "Rows are calculated automatically from the ciphertext length.")

        ciphertext_in = st.text_area(
            "Ciphertext", placeholder="Enter Columnar Transposition ciphertext…",
            height=100, key="col_dec_cipher"
        )
        
        c1, c2 = st.columns(2)
        with c1:
            cols_d = st.number_input("Number of Columns", min_value=1, max_value=100, value=5, key="col_dec_cols")
        with c2:
            key_val_d = st.text_input("Key (Numeric, same as encryption)", placeholder="e.g., 43125", key="col_dec_key")

        if st.button("🔓 Decrypt", key="col_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            if not ok1:
                error_box(e1)
            else:
                # Auto-calculate rows from ciphertext length and cols
                import math
                processed_ct = "".join(ch for ch in ciphertext_in if not ch.isspace())
                rows_d = math.ceil(len(processed_ct) / int(cols_d)) if int(cols_d) > 0 else 1
                ok2, e2 = validate_columnar_params(ciphertext_in, rows_d, int(cols_d), key_val_d, "decrypt")
                if not ok2:
                    error_box(e2)
                else:
                    result = decrypt(ciphertext_in, rows_d, int(cols_d), key_val_d)
                    render_result_table([
                        ("Algorithm", "Columnar Transposition"),
                        ("Ciphertext", ciphertext_in),
                        ("Key", key_val_d),
                        ("Plaintext", result["plaintext"]),
                        ("Decryption Time", format_time(result["time_taken"])),
                    ])
                    render_result_box("🔓 Decrypted Text", result["plaintext"])
                    info_box("Note: Any 'X' padding characters at the end are removed automatically.")
                    copy_text_area("Copy Plaintext", result["plaintext"], "col_dec_copy")
                    download_result(result["plaintext"], "columnar_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Columnar Transposition Cipher

        ### What is it?
        The Columnar Transposition cipher is a transposition cipher where letters of the plaintext
        are rearranged rather than substituted. The plaintext is written row-by-row into a grid
        with a specified number of columns, and then read column-by-column in the order specified
        by the sorted order of the key.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Example: "NETWORKSECURITY" with Key "43125" (Rows = 4, Columns = 5)</strong><br><br>
            Key:      4  3  1  2  5<br>
            Order:    2  3  1  0  4   ← sorted index order (Key '1' is index 2, '2' is index 3, etc.)<br><br>
            N  E  T  W  O<br>
            R  K  S  E  C<br>
            U  R  I  T  Y<br>
            X  X  X  X  X   (padded with X)<br><br>
            Read columns in sorted key index order:<br>
            Col index 2 ('1'): T S I X<br>
            Col index 3 ('2'): W E T X<br>
            Col index 1 ('3'): E K R X<br>
            Col index 0 ('4'): N R U X<br>
            Col index 4 ('5'): O C Y X<br><br>
            Ciphertext: TSIXWETXEKRXNRUXOCYX
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Advantages
            - ✅ Position of characters is completely shuffled
            - ✅ Easy to execute manually with grid diagrams
            - ✅ Used historically in military field communications

            ### Key and Parameters
            - **Rows & Columns** define grid size.
            - **Key** defines permutation sorting order.
            """)
        with col2:
            st.markdown("""
            ### Limitations
            - ❌ Preserves letter frequencies (no substitution confusion)
            - ❌ Vulnerable to anagramming (especially with small grids)
            - ❌ Completely insecure against modern cryptanalysis
            """)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example (Colab Notebook Match)")
        demo_text = "NETWORKSECURITY"
        demo_rows = 4
        demo_cols = 5
        demo_key = "43125"
        st.markdown(f"**Plaintext:** `{demo_text}` | **Rows:** `{demo_rows}` | **Columns:** `{demo_cols}` | **Key:** `{demo_key}`")

        result = encrypt(demo_text, demo_rows, demo_cols, demo_key)
        dec = decrypt(result["ciphertext"], demo_rows, demo_cols, demo_key)

        render_result_table([
            ("Plaintext", demo_text),
            ("Key", demo_key),
            ("Padded Text", result["padded_text"]),
            ("Column Order", str(result["column_order"])),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
        ])
        render_result_box("🔐 Ciphertext", result["ciphertext"])

        st.markdown("##### Grid Layout:")
        render_column_grid(result["grid"], demo_key, result["column_order"])
