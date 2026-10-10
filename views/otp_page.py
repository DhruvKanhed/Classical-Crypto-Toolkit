"""
One-Time Pad (OTP) Cipher Page
"""
import streamlit as st
import pandas as pd
from ciphers.otp import encrypt, decrypt, validate_key
from utils.validators import validate_text_not_empty
from utils.timing import format_time
from views.ui_helpers import (
    render_cipher_header, render_result_box, render_result_table,
    download_result, copy_text_area, info_box, error_box, success_box, warning_box
)


def render():
    render_cipher_header(
        name="One-Time Pad (OTP)",
        cipher_type="Substitution",
        description="Theoretically unbreakable cipher when used correctly. The key must be truly random, at least as long as the message, and never reused. This implementation is a simplified educational demonstration.",
        key_info="Random key ≥ number of alphabetic characters in the message",
        security="High*",
        concept="C_i = (P_i + K_i) mod 26  |  P_i = (C_i − K_i) mod 26",
        icon="🛡️",
    )

    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Educational Demonstration Only:</strong>
        This OTP uses Python's <code>random</code> module which is NOT cryptographically secure.
        A true OTP requires a genuinely random key (e.g., hardware RNG), equal in length to the message,
        used exactly ONCE, and kept completely secret. Do NOT use this for any real security purpose.
    </div>
    """, unsafe_allow_html=True)

    tab_enc, tab_dec, tab_learn, tab_example = st.tabs(
        ["🔒 Encrypt", "🔓 Decrypt", "📖 Learn", "💡 Example"]
    )

    # ── ENCRYPT TAB ────────────────────────────────────────────────────────────
    with tab_enc:
        st.markdown("#### Encrypt Plaintext")

        plaintext = st.text_area(
            "Plaintext", placeholder="Enter text to encrypt…",
            height=100, key="otp_enc_plain"
        )

        otp_key = st.text_input(
            "OTP Key (alphabetic, ≥ message alpha length)",
            placeholder="Enter your OTP key here…",
            key="otp_enc_key",
            help="The key must have at least as many alphabetic characters as the plaintext."
        )

        if otp_key and plaintext:
            ok, err = validate_key(plaintext, otp_key)
            if ok:
                key_alpha = "".join(ch for ch in otp_key if ch.isalpha())
                pt_alpha = sum(1 for ch in plaintext if ch.isalpha())
                success_box(f"Key is valid. Length: {len(key_alpha)} | Plaintext alpha: {pt_alpha}")
            else:
                error_box(err)

        if st.button("🔒 Encrypt", key="otp_enc_btn"):
            ok1, e1 = validate_text_not_empty(plaintext, "Plaintext")
            ok2, e2 = validate_key(plaintext, otp_key) if otp_key else (False, "Key cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = encrypt(plaintext, otp_key)
                dec_result = decrypt(result["ciphertext"], otp_key)

                render_result_table([
                    ("Algorithm", "One-Time Pad (OTP)"),
                    ("Plaintext", plaintext),
                    ("Key Used", result["key_used"]),
                    ("Ciphertext", result["ciphertext"]),
                    ("Verified Decrypt", dec_result["plaintext"]),
                    ("Encryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔐 Ciphertext", result["ciphertext"])

                st.markdown("""
                <div class="warning-box">
                    🔑 <strong>Keep the key secret!</strong> In a real OTP, the key must be:
                    (1) truly random, (2) at least as long as the message, (3) used only once,
                    (4) kept completely secret. Sharing the ciphertext without the key reveals nothing.
                </div>
                """, unsafe_allow_html=True)

                if result["char_table"]:
                    st.markdown("##### Character-by-Character Table")
                    df = pd.DataFrame(
                        result["char_table"],
                        columns=["Plain", "Key Letter", "Shift", "Cipher"]
                    )
                    st.dataframe(df, use_container_width=True, hide_index=True)

                c1, c2 = st.columns(2)
                with c1:
                    copy_text_area("Copy Ciphertext", result["ciphertext"], "otp_enc_copy")
                with c2:
                    download_result(
                        f"Ciphertext:\n{result['ciphertext']}\n\nKey Used:\n{result['key_used']}",
                        "otp_encrypted.txt"
                    )

    # ── DECRYPT TAB ────────────────────────────────────────────────────────────
    with tab_dec:
        st.markdown("#### Decrypt Ciphertext")
        info_box("You must use the exact same key that was used during encryption.")

        ciphertext_in = st.text_area(
            "Ciphertext", placeholder="Enter OTP ciphertext…",
            height=100, key="otp_dec_cipher"
        )

        otp_key_d = st.text_input(
            "OTP Key (same key used for encryption)",
            placeholder="Enter the key…",
            key="otp_dec_key"
        )

        if st.button("🔓 Decrypt", key="otp_dec_btn"):
            ok1, e1 = validate_text_not_empty(ciphertext_in, "Ciphertext")
            ok2, e2 = validate_key(ciphertext_in, otp_key_d) if otp_key_d else (False, "Key cannot be empty.")
            if not ok1:
                error_box(e1)
            elif not ok2:
                error_box(e2)
            else:
                result = decrypt(ciphertext_in, otp_key_d)
                render_result_table([
                    ("Algorithm", "One-Time Pad (OTP)"),
                    ("Ciphertext", ciphertext_in),
                    ("Key Used", result["key_used"]),
                    ("Plaintext", result["plaintext"]),
                    ("Decryption Time", format_time(result["time_taken"])),
                ])
                render_result_box("🔓 Decrypted Text", result["plaintext"])
                copy_text_area("Copy Plaintext", result["plaintext"], "otp_dec_copy")
                download_result(result["plaintext"], "otp_decrypted.txt")

    # ── LEARN TAB ──────────────────────────────────────────────────────────────
    with tab_learn:
        st.markdown("""
        ## 📖 Understanding One-Time Pad (OTP)

        ### What is it?
        The One-Time Pad was invented in 1882 by Frank Miller and rediscovered in 1917 by
        Gilbert Vernam. It is the only cipher proven to be theoretically unbreakable
        (information-theoretically secure) when used correctly.

        ### Why Is It Unbreakable?
        Because the key is truly random and as long as the message, the ciphertext provides
        absolutely no information about the plaintext without the key. Every possible plaintext
        of that length is equally likely given the ciphertext alone.
        """)
        st.markdown("""
        <div class="crypto-card">
            <strong>Four Requirements for a True OTP:</strong><br><br>
            1. 🎲 <strong>Truly Random Key</strong> — Generated by hardware RNG, not a PRNG<br>
            2. 📏 <strong>Key ≥ Message Length</strong> — Each message character needs its own key character<br>
            3. 1️⃣ <strong>Used Only Once</strong> — Reusing a key breaks the security completely<br>
            4. 🔒 <strong>Keep Secret</strong> — The key must be shared through a perfectly secure channel
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Advantages
            - ✅ Theoretically unbreakable when used correctly
            - ✅ No computational assumption (not just hard — impossible)
            - ✅ Simple mathematical operations (XOR/mod 26)

            ### Historical Uses
            - 🔴 Soviet "hot line" during Cold War
            - 🔴 Diplomatic communications
            - 🔴 Espionage (one-time cipher pads)
            """)
        with col2:
            st.markdown("""
            ### Limitations (Practical)
            - ❌ Key must be as long as the message (impractical for large data)
            - ❌ Secure key distribution is extremely difficult
            - ❌ Reusing a key (two-time pad) completely breaks security
            - ❌ Quantum computers cannot help — OTP is information-theoretically secure

            ### What Breaks OTP in Practice?
            - **Key reuse** — The greatest practical weakness
            - **Pseudo-random key** — Predictable keys compromise security
            - **Key interception** — Key distribution channel must be perfectly secure
            """)

        st.markdown("### Security Level")
        st.markdown('<div class="success-box">🟢 <strong>HIGH* (when used correctly)</strong> — '
                    'Theoretically unbreakable. The asterisk indicates practical limitations: '
                    'secure key distribution and key length requirements make true OTP impractical for modern use.</div>',
                    unsafe_allow_html=True)

    # ── EXAMPLE TAB ────────────────────────────────────────────────────────────
    with tab_example:
        st.markdown("### 💡 Worked Example")
        demo_plain = "HELLO"
        demo_key = "XMCKL"
        st.markdown(f"**Plaintext:** `{demo_plain}`  |  **Key:** `{demo_key}`")

        result = encrypt(demo_plain, demo_key)
        dec = decrypt(result["ciphertext"], demo_key)

        render_result_table([
            ("Plaintext", demo_plain),
            ("Key", demo_key),
            ("Ciphertext", result["ciphertext"]),
            ("Decrypted", dec["plaintext"]),
            ("Round-Trip", "✅ SUCCESS" if dec["plaintext"] == demo_plain else "❌ FAILED"),
        ])
        render_result_box("🔐 Ciphertext", result["ciphertext"])

        df = pd.DataFrame(
            result["char_table"],
            columns=["Plain", "Key Letter", "Shift", "Cipher"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

