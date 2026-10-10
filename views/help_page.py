"""
Help / User Manual Page
"""
import streamlit as st


def render():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem 0;">
        <div class="app-title" style="font-size:1.6rem;">❓ Help / User Manual</div>
        <p style="color:#94a3b8;margin-top:0.5rem;">
            How to use the Classical Cryptography Toolkit
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Start ────────────────────────────────────────────────────────────
    st.markdown("## 🚀 Quick Start Guide")

    steps = [
        ("1️⃣", "Select an Algorithm", "Use the sidebar to navigate to any cipher page (e.g., Caesar Cipher, Vigenère Cipher)."),
        ("2️⃣", "Enter Plaintext or Ciphertext", "Type or paste your text in the input field. For encryption, enter plaintext. For decryption, enter ciphertext."),
        ("3️⃣", "Enter or Generate the Key", "Each algorithm requires a specific type of key. Use the 'Generate Key' button (where available) or enter your own key."),
        ("4️⃣", "Click Encrypt or Decrypt", "Press the Encrypt or Decrypt button to process your text."),
        ("5️⃣", "View the Result", "The output is displayed in a result table and highlighted box. Review the character-by-character working table if shown."),
        ("6️⃣", "Review the Working Steps", "Expand the step tables to understand how the cipher processed each character."),
        ("7️⃣", "Download the Result", "Use the Download button to save the encrypted/decrypted text as a .txt file."),
    ]

    for icon, title, desc in steps:
        st.markdown(f"""
        <div class="crypto-card" style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:0.75rem;">
            <div style="font-size:1.8rem;flex-shrink:0;">{icon}</div>
            <div>
                <div style="font-weight:700;color:#e2e8f0;margin-bottom:0.25rem;">{title}</div>
                <div style="color:#94a3b8;font-size:0.88rem;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Key Reference ─────────────────────────────────────────────────────────
    st.markdown("## 🔑 Key Reference Guide")
    st.markdown("Each algorithm requires a different type of key:")

    key_data = [
        ("Caesar Cipher", "🔡", "Integer (0–25)", "Shift = 3 means A→D, B→E, etc.", "Any integer works; applied mod 26"),
        ("Monoalphabetic", "🔤", "26-letter permutation", "QWERTYUIOPASDFGHJKLZXCVBNM", "All 26 letters, each exactly once"),
        ("Playfair Cipher", "🔲", "Keyword (any word)", "SECURITY", "Used to build the 5×5 matrix; J treated as I"),
        ("Hill Cipher", "🔢", "2×2 integer matrix", "[[3,3],[2,5]]", "det(K) must be coprime with 26; use presets if unsure"),
        ("Vigenère Cipher", "🗝️", "Alphabetic keyword", "LEMON", "Repeated to match plaintext length"),
        ("One-Time Pad", "🛡️", "Random alphabetic key", "Auto-generated", "Must be ≥ alpha character count of message"),
        ("Rail Fence", "🚂", "Number of rails", "3", "Integer ≥ 2; must be less than text length"),
        ("Columnar Trans.", "📊", "Alphabetic keyword", "ZEBRA", "Determines column reading order"),
    ]

    for name, icon, key_type, example, note in key_data:
        col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 2])
        with col1:
            st.markdown(f"**{icon} {name}**")
        with col2:
            st.markdown(f"`{key_type}`")
        with col3:
            st.markdown(f"e.g., `{example}`")
        with col4:
            st.markdown(f"_{note}_")
        st.markdown("<hr style='margin:0.3rem 0;border-color:#1e3a5f;'>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabs Explanation ─────────────────────────────────────────────────────
    st.markdown("## 📑 Understanding the Cipher Page Tabs")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="crypto-card" style="text-align:center;">
            <div style="font-size:1.5rem;">🔒</div>
            <strong>Encrypt</strong><br>
            <small style="color:#94a3b8;">Enter plaintext + key → get ciphertext</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="crypto-card" style="text-align:center;">
            <div style="font-size:1.5rem;">🔓</div>
            <strong>Decrypt</strong><br>
            <small style="color:#94a3b8;">Enter ciphertext + key → recover plaintext</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="crypto-card" style="text-align:center;">
            <div style="font-size:1.5rem;">📖</div>
            <strong>Learn</strong><br>
            <small style="color:#94a3b8;">Educational explanation, formula, attacks</small>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="crypto-card" style="text-align:center;">
            <div style="font-size:1.5rem;">💡</div>
            <strong>Example</strong><br>
            <small style="color:#94a3b8;">Worked example with known test vectors</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── FAQ ───────────────────────────────────────────────────────────────────
    st.markdown("## ❓ Frequently Asked Questions")

    faqs = [
        ("Why does decryption not return the exact original plaintext for some ciphers?",
         "Some ciphers (Playfair, Hill) remove non-alphabetic characters and apply preprocessing. "
         "The decrypted text represents the processed version. Padding characters (X) may also appear "
         "in Playfair/Columnar decryption — these can be removed manually."),
        ("What does 'J is treated as I' mean in Playfair?",
         "The 5×5 Playfair matrix has only 25 cells (5×5) but there are 26 letters. To fit, "
         "I and J are merged into one cell. Any J in your plaintext is automatically treated as I."),
        ("Why can't I use some matrices for Hill Cipher?",
         "The Hill Cipher requires the matrix to be invertible modulo 26. This means "
         "det(K) mod 26 must be non-zero AND gcd(det(K), 26) must equal 1. Use the preset "
         "matrices provided if you're unsure."),
        ("Is OTP truly unbreakable?",
         "Theoretically YES — but only when (1) the key is truly random, (2) the key is at least "
         "as long as the message, (3) the key is never reused, and (4) the key is kept perfectly secret. "
         "This educational implementation uses Python's random module which is NOT cryptographically secure."),
        ("Can I encrypt files with special characters?",
         "Yes, but some algorithms (Playfair, Hill) only process alphabetic characters. "
         "Others (Caesar, Vigenère, OTP, Rail Fence, Columnar) preserve non-alphabetic characters."),
        ("How do I copy the output?",
         "A 'Copy' text area is provided below each result. Click inside the box and select all (Ctrl+A), "
         "then copy (Ctrl+C). Alternatively, use the Download button to save as a .txt file."),
    ]

    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(a)

    st.markdown("---")

    # ── Security Note ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="warning-box">
        🔒 <strong>Important Security Note:</strong> This toolkit demonstrates classical cryptography
        for educational purposes. Classical ciphers (Caesar, Playfair, Vigenère, Hill, Rail Fence, etc.)
        are NOT secure for protecting modern sensitive information. Use AES, RSA, or other modern
        algorithms for any real security application.
    </div>
    """, unsafe_allow_html=True)

