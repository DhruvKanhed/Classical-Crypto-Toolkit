"""
File Encryption / Decryption Page
"""
import streamlit as st
from utils.file_handler import read_uploaded_file, create_download_content, get_file_stats
from utils.timing import format_time

# Import all encryption functions
from ciphers.caesar import encrypt as caesar_enc, decrypt as caesar_dec
from ciphers.monoalphabetic import encrypt as mono_enc, decrypt as mono_dec, generate_key as mono_gen
from ciphers.playfair import encrypt as pf_enc, decrypt as pf_dec
from ciphers.hill import encrypt as hill_enc, decrypt as hill_dec
from ciphers.vigenere import encrypt as vig_enc, decrypt as vig_dec
from ciphers.otp import encrypt as otp_enc, decrypt as otp_dec, generate_key as otp_gen
from ciphers.rail_fence import encrypt as rf_enc, decrypt as rf_dec
from ciphers.columnar import encrypt as col_enc, decrypt as col_dec

from utils.validators import (
    validate_caesar_key, validate_mono_key, validate_playfair_key,
    validate_hill_matrix, validate_vigenere_key, validate_otp_key,
    validate_columnar_params
)
from views.ui_helpers import info_box, warning_box, error_box, success_box


ALGORITHMS = [
    "Caesar Cipher",
    "Monoalphabetic Cipher",
    "Playfair Cipher",
    "Hill Cipher",
    "Vigenère Cipher",
    "One-Time Pad",
    "Rail Fence Cipher",
    "Columnar Transposition",
]


def render_key_input(algo: str, mode: str, file_content: str = "") -> tuple[bool, str, any]:
    """
    Render key input controls for the selected algorithm.
    Returns (is_valid, error_msg, key_data).
    """
    prefix = f"file_{algo.replace(' ', '_')}_{mode}"

    if algo == "Caesar Cipher":
        shift = st.number_input("Shift Key", min_value=0, max_value=25, value=3, key=f"{prefix}_shift")
        return True, "", int(shift)

    elif algo == "Monoalphabetic Cipher":
        col1, col2 = st.columns([3, 1])
        with col1:
            key = st.text_input("Substitution Key (26 letters)", key=f"{prefix}_key",
                                placeholder="QWERTYUIOPASDFGHJKLZXCVBNM", max_chars=26)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎲 Generate", key=f"{prefix}_gen", use_container_width=True):
                st.session_state[f"{prefix}_key"] = mono_gen()
                st.rerun()
        ok, err = validate_mono_key(key) if key else (False, "Key required.")
        return ok, err, key

    elif algo == "Playfair Cipher":
        kw = st.text_input("Keyword", key=f"{prefix}_kw", placeholder="e.g., SECURITY")
        ok, err = validate_playfair_key(kw) if kw else (False, "Keyword required.")
        return ok, err, kw

    elif algo == "Hill Cipher":
        c1, c2 = st.columns(2)
        with c1:
            a = st.number_input("K[0][0]", value=3, key=f"{prefix}_a")
            c_v = st.number_input("K[1][0]", value=2, key=f"{prefix}_c")
        with c2:
            b = st.number_input("K[0][1]", value=3, key=f"{prefix}_b")
            d = st.number_input("K[1][1]", value=5, key=f"{prefix}_d")
        vals = [int(a), int(b), int(c_v), int(d)]
        ok, err = validate_hill_matrix(vals)
        return ok, err, vals

    elif algo == "Vigenère Cipher":
        kw = st.text_input("Keyword", key=f"{prefix}_kw", placeholder="e.g., LEMON")
        ok, err = validate_vigenere_key(kw) if kw else (False, "Keyword required.")
        return ok, err, kw

    elif algo == "One-Time Pad":
        warning_box("For file encryption with OTP, a key will be auto-generated. "
                    "For decryption, paste the key that was generated during encryption.")
        if mode == "encrypt":
            return True, "", None  # key generated on-the-fly
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                key = st.text_input("OTP Key (from encryption)", key=f"{prefix}_key")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🎲 Generate", key=f"{prefix}_gen", use_container_width=True):
                    st.session_state[f"{prefix}_key"] = "PLEASEPASTETHEREALKEY"
                    st.rerun()
            return (True, "", key) if key else (False, "Key required for decryption.", "")

    elif algo == "Rail Fence Cipher":
        rails = st.number_input("Number of Rails", min_value=2, max_value=20, value=3, key=f"{prefix}_rails")
        return True, "", int(rails)

    elif algo == "Columnar Transposition":
        c1, c2 = st.columns(2)
        with c1:
            cols = st.number_input("Number of Columns", min_value=1, max_value=1000, value=5, key=f"{prefix}_cols")
        with c2:
            key = st.text_input("Key (Numeric, length must equal columns)", key=f"{prefix}_key", placeholder="e.g., 43125")
        
        # Calculate row dimensions dynamically based on input length
        processed_text = "".join(ch for ch in file_content if not ch.isspace())
        rows = max(1, (len(processed_text) + cols - 1) // cols) if mode == "encrypt" else max(1, len(processed_text) // cols)
        
        ok, err = validate_columnar_params(file_content, rows, cols, key, mode)
        return ok, err, {"rows": rows, "cols": cols, "key": key}

    return False, "Unknown algorithm.", None


def run_encrypt(algo: str, text: str, key) -> dict:
    """Run encryption for the given algorithm."""
    if algo == "Caesar Cipher":
        return caesar_enc(text, key)
    elif algo == "Monoalphabetic Cipher":
        return mono_enc(text, key)
    elif algo == "Playfair Cipher":
        return pf_enc(text, key)
    elif algo == "Hill Cipher":
        return hill_enc(text, key)
    elif algo == "Vigenère Cipher":
        return vig_enc(text, key)
    elif algo == "One-Time Pad":
        generated_key = otp_gen(text)
        result = otp_enc(text, generated_key)
        result["generated_key"] = generated_key
        return result
    elif algo == "Rail Fence Cipher":
        return rf_enc(text, key)
    elif algo == "Columnar Transposition":
        return col_enc(text, key["rows"], key["cols"], key["key"])
    raise ValueError(f"Unknown algorithm: {algo}")


def run_decrypt(algo: str, text: str, key) -> dict:
    """Run decryption for the given algorithm."""
    if algo == "Caesar Cipher":
        return caesar_dec(text, key)
    elif algo == "Monoalphabetic Cipher":
        return mono_dec(text, key)
    elif algo == "Playfair Cipher":
        return pf_dec(text, key)
    elif algo == "Hill Cipher":
        return hill_dec(text, key)
    elif algo == "Vigenère Cipher":
        return vig_dec(text, key)
    elif algo == "One-Time Pad":
        return otp_dec(text, key)
    elif algo == "Rail Fence Cipher":
        return rf_dec(text, key)
    elif algo == "Columnar Transposition":
        return col_dec(text, key["rows"], key["cols"], key["key"])
    raise ValueError(f"Unknown algorithm: {algo}")


def render():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem 0;">
        <div class="app-title" style="font-size:1.6rem;">📂 File Encryption / Decryption</div>
        <p style="color:#94a3b8;margin-top:0.5rem;">
            Upload a .txt file, choose an algorithm, and encrypt or decrypt it
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow steps
    st.markdown("""
    <div class="info-box">
        📋 <strong>Workflow:</strong>
        Upload File → Select Algorithm → Enter Key → Encrypt / Decrypt → Preview → Download
    </div>
    """, unsafe_allow_html=True)

    # ── File Upload ───────────────────────────────────────────────────────────
    st.markdown("### 📁 Step 1: Upload File")
    uploaded_file = st.file_uploader(
        "Upload a .txt file",
        type=["txt"],
        key="file_upload",
        help="Only plain text (.txt) files encoded in UTF-8 are supported."
    )

    file_content = ""
    if uploaded_file is not None:
        ok, content, err = read_uploaded_file(uploaded_file)
        if not ok:
            error_box(err)
        else:
            file_content = content
            stats = get_file_stats(content)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Characters", stats["character_count"])
            col2.metric("Words", stats["word_count"])
            col3.metric("Lines", stats["line_count"])
            col4.metric("Alpha Chars", stats["alpha_count"])

            with st.expander("📄 Preview File Content"):
                preview = content[:2000] + ("\n…(truncated)" if len(content) > 2000 else "")
                st.text(preview)

    # ── Algorithm Selection ───────────────────────────────────────────────────
    st.markdown("### 🔐 Step 2: Select Algorithm")
    algo = st.selectbox("Choose algorithm:", ALGORITHMS, key="file_algo")

    # ── Operation Selection ───────────────────────────────────────────────────
    st.markdown("### ⚙️ Step 3: Configure Key")
    operation = st.radio("Operation:", ["🔒 Encrypt", "🔓 Decrypt"],
                         horizontal=True, key="file_op")
    mode = "encrypt" if "Encrypt" in operation else "decrypt"

    key_valid, key_err, key_data = render_key_input(algo, mode, file_content)

    # ── Process ───────────────────────────────────────────────────────────────
    st.markdown("### 🚀 Step 4: Process")
    if st.button(f"{'🔒 Encrypt' if mode == 'encrypt' else '🔓 Decrypt'} File",
                 key="file_process_btn", use_container_width=False):
        if not file_content:
            error_box("Please upload a file first.")
        elif not key_valid:
            error_box(key_err)
        else:
            try:
                with st.spinner(f"{'Encrypting' if mode == 'encrypt' else 'Decrypting'}…"):
                    if mode == "encrypt":
                        result = run_encrypt(algo, file_content, key_data)
                        output_text = result.get("ciphertext", result.get("plaintext", ""))
                        suffix = "_encrypted"
                    else:
                        result = run_decrypt(algo, file_content, key_data)
                        output_text = result.get("plaintext", result.get("ciphertext", ""))
                        suffix = "_decrypted"

                elapsed = result.get("time_taken", 0.0)

                success_box(f"{'Encryption' if mode == 'encrypt' else 'Decryption'} complete! "
                            f"Time: {format_time(elapsed)}")

                # Show OTP generated key
                if algo == "One-Time Pad" and mode == "encrypt" and "generated_key" in result:
                    st.markdown(f"""
                    <div class="warning-box">
                        🔑 <strong>Generated OTP Key (SAVE THIS for decryption!):</strong><br>
                        <code style="word-break:break-all;">{result["generated_key"]}</code>
                    </div>
                    """, unsafe_allow_html=True)

                # Output preview
                st.markdown("### 📄 Step 5: Preview & Download Output")
                with st.expander("📄 Output Preview", expanded=True):
                    preview = output_text[:2000] + ("\n…(truncated)" if len(output_text) > 2000 else "")
                    st.text(preview)

                # Stats
                in_stats = get_file_stats(file_content)
                out_stats = get_file_stats(output_text)
                c1, c2, c3 = st.columns(3)
                c1.metric("Input Characters", in_stats["character_count"])
                c2.metric("Output Characters", out_stats["character_count"])
                c3.metric("Processing Time", format_time(elapsed))

                # Download button
                base_name = (uploaded_file.name if uploaded_file else "file").rsplit(".", 1)[0]
                out_filename = f"{base_name}{suffix}.txt"
                st.download_button(
                    label=f"⬇️ Download {out_filename}",
                    data=output_text.encode("utf-8"),
                    file_name=out_filename,
                    mime="text/plain",
                    use_container_width=True,
                )

            except Exception as e:
                error_box(f"Processing error: {str(e)}")

    # Notes
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        📝 <strong>Notes:</strong><br>
        • Some algorithms (Playfair, Hill) remove or modify non-alphabetic characters.<br>
        • OTP generates a new random key each time — save the key to be able to decrypt later.<br>
        • For large files, processing may take a moment.<br>
        • Download the output file after processing.
    </div>
    """, unsafe_allow_html=True)

