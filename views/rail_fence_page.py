"""
Rail Fence Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.rail_fence import encrypt, decrypt
from utils.validators import validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box
)


def render_zigzag(visual_grid: list[list[str]], max_cols: int = 40):
    """Render the zigzag grid visually using HTML."""
    # Limit display width
    grid_to_show = [row[:max_cols] for row in visual_grid]
    truncated = len(visual_grid[0]) > max_cols

    rows_html = []
    for rail_idx, row in enumerate(grid_to_show):
        cells = []
        for ch in row:
            if ch != '.':
                cells.append(f'<td class="matrix-cell" style="min-width:32px;height:32px;font-size:0.85rem;">{ch}</td>')
            else:
                cells.append('<td style="min-width:32px;height:32px;border:none;background:transparent;"></td>')
        rows_html.append(
            f'<tr><td style="color:#64748b;font-size:0.75rem;padding-right:0.5rem;font-family:monospace;">Rail {rail_idx}</td>'
            + "".join(cells) + "</tr>"
        )

    html = f"""
    <div style="overflow-x:auto;">
        <table style="border-collapse:separate;border-spacing:2px;">
            <tbody>
                {"".join(rows_html)}
            </tbody>
        </table>
        {"<p style='color:#64748b;font-size:0.8rem;'>⋯ (truncated for display, showing first 40 chars)</p>" if truncated else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render():
    render_cipher_header(
        name="Rail Fence Cipher",
        cipher_type="Transposition",
        description="A transposition cipher that writes the plaintext in a zigzag pattern across a set of imaginary 'rails' (rows), then reads each rail left-to-right to form the ciphertext.",
        key_info="Number of rails (integer ≥ 2)",
        security="Low",
        concept="Write text diagonally across rails → read rail by rail",
        icon="🚂",
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
                height=100, key="rf_enc_plain"
            )
        with col2:
            rails = st.number_input(
                "Number of Rails", min_value=2, max_value=20, value=3,
                step=1, key="rf_enc_rails",
                help="Number of horizontal rails in the zigzag pattern."
            )

        if plaintext and rails >= 2:
            try:
                preview = encrypt(plaintext, int(rails))
                st.markdown("**Zigzag Visualization:**")
                render_zigzag(preview["visual_grid"])
            except Exception:
                pass

        if st.button("🔒 Encrypt", key="rf_enc_btn"):
            ok, err = validate_text_not_empty(plaintext, "Plaintext")
            if not ok:
                error_box(err)
            elif int(rails) < 2:
                error_box("Number of rails must be at least 2.")
            else:
                result = encrypt(plaintext, int(rails))
                dec_result = decrypt(result["ciphertext"], int(rails))

                render_result_table([
                    ("Algorithm", "Rail Fence Cipher"),
                    ("Plaintext", plaintext),
                    ("Number of Rails", str(rails)),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])

                # Rail breakdown
                st.markdown("##### Contents of Each Rail")
                rail_data = [(f"Rail {i}", r_str) for i, r_str in enumerate(result["rail_strings"])]
                df = pd.DataFrame(rail_data, columns=["Rail", "Characters"])
                st.dataframe(df, use_container_width=True, hide_index=True)

                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "rf_enc_copy")
                with c2:
                    download_result(result["ciphertext"], "railfence_encrypted.txt")

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        col1, col2 = st.columns([3, 1])
        with col1:
            ciphertext_in = st.text_area(
                "Ciphertext", placeholder="Enter Rail Fence ciphertext…",
                height=100, key="rf_dec_cipher"
            )
        with col2:
            rails_d = st.number_input(
                "Number of Rails (same as encryption)", min_value=2, max_value=20,
                value=3, step=1, key="rf_dec_rails"
            )

        if st.button("🔓 Decrypt", key="rf_dec_btn"):
            ok, err = validate_text_not_empty(ciphertext_in, "Ciphertext")
            if not ok:
                error_box(err)
            else:
                result = decrypt(ciphertext_in, int(rails_d))
                render_result_table([
                    ("Algorithm", "Rail Fence Cipher"),
                    ("Ciphertext", ciphertext_in),
                    ("Number of Rails", str(rails_d)),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Text", result["plaintext"])
                copy_text_area("Copy Plaintext", result["plaintext"], "rf_dec_copy")
                download_result(result["plaintext"], "railfence_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding Rail Fence Cipher

        ### What is it?
        The Rail Fence Cipher is a classic transposition cipher. Unlike substitution ciphers
        (which replace letters), transposition ciphers rearrange the letters in the message.
        The Rail Fence cipher writes the message in a zigzag across imaginary horizontal "rails",
        then reads across each rail to form the ciphertext.

        ### How does it work?
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Example: "WEAREDISCOVEREDFLEEATONCE" with 3 rails</strong><br><br>
            Rail 0: W . . . E . . . I . . . V . . . D . . . E . . . C .<br>
            Rail 1: . E . R . D . S . O . E . E . F . E . A . O . C . E<br>
            Rail 2: . . A . . . . . C . . . R . . . L . . . T . . . N . .<br><br>
            Rail 0: WEIDEC<br>
            Rail 1: ERDSOEEFEA OCE<br>
            Rail 2: ACRLTNE<br><br>
            Ciphertext = Rail0 + Rail1 + Rail2 = WEIDECERDSOEEF EAOCACRLTNE
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Advantages
            - ✅ Simple to understand and implement
            - ✅ Hides word boundaries and letter order
            - ✅ Can be combined with substitution ciphers

            ### Required Key
            Just a single integer: the number of rails.
            Typical values: 2, 3, 4 rails.
            """)
        with col2:
            st.markdown("""
            ### Limitations
            - ❌ Very few possible key values (limited by text length)
            - ❌ Pattern analysis reveals the rail count
            - ❌ Does not change letter frequencies (only positions)
            - ❌ Can be broken by brute-force trying all rail values

            ### Common Attacks
            - **Brute Force:** Try all possible rail values (usually < 20)
            - **Pattern Analysis:** Known word patterns reveal structure
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="error-box">🔴 <strong>LOW</strong> — '
                    'Rail Fence provides minimal security. The small key space and preserved '
                    'letter frequencies make it trivial to break.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        demo_text = "WEAREDISCOVEREDFLEEATONCE"
        demo_rails = 3
        st.markdown(f"**Plaintext:** `{demo_text}`  |  **Rails:** `{demo_rails}`")

        result = encrypt(demo_text, demo_rails)
        dec = decrypt(result["ciphertext"], demo_rails)

        render_result_table([
            ("Plaintext", demo_text),
            ("Number of Rails", str(demo_rails)),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
        ])

        st.markdown("##### Zigzag Visualization:")
        render_zigzag(result["visual_grid"])

        st.markdown("##### Rail Contents:")
        for i, r in enumerate(result["rail_strings"]):
            st.markdown(f"- **Rail {i}:** `{r}`")

