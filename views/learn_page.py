"""
Learn Algorithms Page — Educational content for all 8 ciphers
"""
import streamlit as st


ALGORITHMS = [
    {
        "name": "Caesar Cipher",
        "icon": "🔡",
        "type": "Substitution",
        "security": "Low",
        "what": "A substitution cipher that shifts each letter a fixed number of positions in the alphabet. Named after Julius Caesar who used it in personal correspondence.",
        "how": [
            "Convert each plaintext letter to its numerical position (A=0, B=1, ..., Z=25)",
            "Add the shift key K to each position",
            "Apply modulo 26 to wrap around the alphabet",
            "Convert back to a letter",
        ],
        "input": "Any text. Non-alphabetic characters are preserved unchanged.",
        "key": "A single integer K (typically 0–25). With K=13, it becomes ROT13.",
        "formula": "Encrypt: C = (P + K) mod 26\nDecrypt: P = (C − K) mod 26",
        "example": {"plain": "HELLO", "key": "K=3", "cipher": "KHOOR", "decrypt": "HELLO"},
        "advantages": ["Simple to understand", "Fast to compute", "Good teaching tool"],
        "limitations": ["Only 25 possible keys (easily brute-forced)", "Letter frequencies preserved", "No real security"],
        "attacks": ["Brute Force (try all 25 shifts)", "Frequency Analysis"],
    },
    {
        "name": "Monoalphabetic Cipher",
        "icon": "🔤",
        "type": "Substitution",
        "security": "Low",
        "what": "Each letter of the plaintext alphabet maps to a unique different letter in the ciphertext alphabet using a fixed permutation. Every occurrence of a letter always maps to the same cipher letter.",
        "how": [
            "Create a permutation of all 26 letters (the key)",
            "Build a lookup table: A→?, B→?, ..., Z→?",
            "Replace each plaintext letter with its cipher equivalent",
            "To decrypt, reverse the lookup table",
        ],
        "input": "Any text. Non-alphabetic characters are preserved unchanged.",
        "key": "A permutation of all 26 letters (e.g., QWERTYUIOPASDFGHJKLZXCVBNM).",
        "formula": "Each plain letter P maps to a fixed cipher letter C via a substitution table.",
        "example": {"plain": "HELLO", "key": "QWERTYUIOPASDFGHJKLZXCVBNM", "cipher": "ITSSG", "decrypt": "HELLO"},
        "advantages": ["26! ≈ 4×10²⁶ possible keys", "More complex than Caesar", "Easy to implement"],
        "limitations": ["Vulnerable to frequency analysis", "Letter frequencies still preserved", "Common words/patterns reveal structure"],
        "attacks": ["Frequency Analysis (match cipher letters to E, T, A...)", "Pattern Analysis", "Known Plaintext Attack"],
    },
    {
        "name": "Playfair Cipher",
        "icon": "🔲",
        "type": "Substitution",
        "security": "Medium",
        "what": "The first digraph substitution cipher. Encrypts pairs of letters (digraphs) instead of single letters using a 5×5 matrix constructed from a keyword. I and J are treated as the same letter.",
        "how": [
            "Build a 5×5 matrix from the keyword (remove duplicates, fill with remaining letters, J→I)",
            "Preprocess plaintext: keep alpha, uppercase, J→I, insert X between repeated pairs, pad to even length",
            "Split into digraphs (pairs)",
            "For each digraph: apply one of 3 rules (same row, same column, rectangle)",
        ],
        "input": "Alphabetic text only (J treated as I). Non-alpha characters removed.",
        "key": "A keyword (any word). Builds the 5×5 matrix.",
        "formula": "Rule 1 (Same Row): shift right | Rule 2 (Same Col): shift down | Rule 3 (Rectangle): swap corners",
        "example": {"plain": "NETWORK", "key": "SECURITY", "cipher": "(depends on matrix)", "decrypt": "NETWORK"},
        "advantages": ["Digraph encryption defeats simple frequency analysis", "Used in WWI/WWII", "More complex than monoalphabetic"],
        "limitations": ["Only 25×25=625 digraph pairs to analyze", "Vulnerable to digraph frequency analysis", "Reversible preprocessing rules known"],
        "attacks": ["Digraph Frequency Analysis", "Known Plaintext Attack", "Pattern Matching"],
    },
    {
        "name": "Hill Cipher",
        "icon": "🔢",
        "type": "Substitution",
        "security": "Medium",
        "what": "A polygraphic substitution cipher that uses linear algebra. Encrypts multiple letters simultaneously using matrix multiplication modulo 26. This implementation uses 2×2 matrices.",
        "how": [
            "Convert plaintext pairs to numerical vectors [P1, P2]",
            "Multiply by the key matrix K: C = K × P",
            "Apply modulo 26",
            "Convert resulting vector back to letters",
            "Decrypt: compute K⁻¹ mod 26, then P = K⁻¹ × C mod 26",
        ],
        "input": "Any text (non-alpha removed). Padded with X if odd length.",
        "key": "A 2×2 matrix of integers. det(K) must be non-zero and coprime with 26.",
        "formula": "Encrypt: C = (K × P) mod 26\nDecrypt: P = (K⁻¹ × C) mod 26",
        "example": {"plain": "HELP", "key": "[[3,3],[2,5]]", "cipher": "HIAT", "decrypt": "HELP"},
        "advantages": ["Encrypts multiple letters at once", "Good diffusion of statistics", "Matrix-based key space"],
        "limitations": ["Not all matrices are valid keys", "Vulnerable to known-plaintext attack", "Matrix inversion required"],
        "attacks": ["Known Plaintext Attack", "Linear Algebra Attack (with 2+ digraphs)"],
    },
    {
        "name": "Vigenère Cipher",
        "icon": "🗝️",
        "type": "Substitution",
        "security": "Medium",
        "what": "A polyalphabetic substitution cipher that uses a repeating keyword. Each keyword letter defines a different Caesar shift for the corresponding plaintext letter. Considered unbreakable for 300 years.",
        "how": [
            "Choose a keyword",
            "Repeat the keyword to match the length of the plaintext alphabetic characters",
            "For each plaintext letter, apply Caesar shift equal to the corresponding key letter value",
            "Decrypt by subtracting the key letters instead",
        ],
        "input": "Any text. Non-alphabetic characters preserved without consuming a key character.",
        "key": "An alphabetic keyword (e.g., LEMON). Repeated as needed.",
        "formula": "Encrypt: C_i = (P_i + K_i) mod 26\nDecrypt: P_i = (C_i − K_i) mod 26",
        "example": {"plain": "ATTACKATDAWN", "key": "LEMON", "cipher": "LXFOPVEFRNHR", "decrypt": "ATTACKATDAWN"},
        "advantages": ["Different shifts per letter — defeats simple frequency analysis", "Large effective key space", "Was 'unbreakable' for centuries"],
        "limitations": ["Kasiski test finds key length", "Once key length known: reduces to multiple Caesars", "Short keywords are weak"],
        "attacks": ["Kasiski Examination", "Index of Coincidence", "Frequency Analysis after key length found"],
    },
    {
        "name": "One-Time Pad",
        "icon": "🛡️",
        "type": "Substitution",
        "security": "High*",
        "what": "The only cipher proven to be information-theoretically secure. Uses a truly random key equal to the message length, used only once. The educational demonstration uses Python's random module (not cryptographically secure).",
        "how": [
            "Generate a truly random key (same length as message alphabetic characters)",
            "For each plaintext letter, add the corresponding key letter (mod 26)",
            "Decrypt by subtracting the key letters",
            "Destroy the key after use (never reuse!)",
        ],
        "input": "Any text. Non-alphabetic characters preserved without consuming a key character.",
        "key": "A random key string with at least as many alpha chars as the message.",
        "formula": "Encrypt: C_i = (P_i + K_i) mod 26\nDecrypt: P_i = (C_i − K_i) mod 26",
        "example": {"plain": "HELLO", "key": "XMCKL", "cipher": "EQNVZ", "decrypt": "HELLO"},
        "advantages": ["Mathematically proven to be unbreakable with a true random key", "Simple operations", "No computational assumptions needed"],
        "limitations": ["Key must be truly random (hard to achieve)", "Key must be as long as the message", "Key can never be reused", "Secure key distribution is practically difficult"],
        "attacks": ["Key Reuse (two-time pad attack)", "Non-random Key (PRNG weakness)", "Key Interception during distribution"],
    },
    {
        "name": "Rail Fence Cipher",
        "icon": "🚂",
        "type": "Transposition",
        "security": "Low",
        "what": "A transposition cipher that writes the plaintext in a zigzag pattern across multiple horizontal 'rails', then reads each rail left-to-right to produce the ciphertext.",
        "how": [
            "Choose a number of rails (e.g., 3)",
            "Write the plaintext diagonally: down and then up, bouncing between rails",
            "Each rail collects the letters that fall on it",
            "Concatenate all rails to form the ciphertext",
            "To decrypt: figure out which positions belong to which rail, then reconstruct",
        ],
        "input": "Any text including spaces and special characters.",
        "key": "A single integer: number of rails (≥ 2).",
        "formula": "No mathematical formula — the key is the geometric pattern of the zigzag.",
        "example": {"plain": "HELLO WORLD", "key": "3 rails", "cipher": "HOREL LWDLO", "decrypt": "HELLO WORLD"},
        "advantages": ["Simple to understand and visualize", "Can be combined with substitution ciphers", "Adds positional confusion"],
        "limitations": ["Very small key space (limited by text length)", "Letter frequencies unchanged", "Trivial to brute-force"],
        "attacks": ["Brute Force (try all rail values)", "Pattern Analysis"],
    },
    {
        "name": "Columnar Transposition",
        "icon": "📊",
        "type": "Transposition",
        "security": "Medium",
        "what": "A transposition cipher that writes plaintext into a grid row-by-row, then reads the columns in the alphabetical order of the keyword letters. Provides more complex rearrangement than Rail Fence.",
        "how": [
            "Write the plaintext into a grid with number of columns = keyword length",
            "Pad last row with X if necessary",
            "Number each column based on alphabetical order of keyword letters",
            "Read each column from top to bottom, in column-number order",
            "To decrypt: reconstruct the grid column-by-column, then read row-by-row",
        ],
        "input": "Any text. Padded with 'X' if the last row is incomplete.",
        "key": "A keyword (e.g., ZEBRA). Column reading order determined by alphabetical rank.",
        "formula": "No formula — rearrangement based on keyword alphabetical order of columns.",
        "example": {"plain": "ATTACKATDAWN", "key": "ZEBRA", "cipher": "(column-ordered ciphertext)", "decrypt": "ATTACKATDAWNX"},
        "advantages": ["Better security than Rail Fence", "Used in WWI/WWII", "Double transposition is significantly stronger"],
        "limitations": ["Letter frequencies unchanged", "Vulnerable to anagramming with short keys", "Known-plaintext reveals key"],
        "attacks": ["Anagramming Columns", "Multiple Anagramming", "Known Plaintext Attack"],
    },
]


def render():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem 0;">
        <div class="app-title" style="font-size:1.6rem;">📚 Learn Classical Cryptography</div>
        <p style="color:#94a3b8;margin-top:0.5rem;">
            Student-friendly explanations of all 8 classical encryption algorithms
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Algorithm selector
    algo_names = [f"{a['icon']} {a['name']}" for a in ALGORITHMS]
    selected = st.selectbox("Select an algorithm to learn:", algo_names, key="learn_select")
    algo = ALGORITHMS[algo_names.index(selected)]

    st.markdown("---")

    # ── Algorithm Card ────────────────────────────────────────────────────────
    type_class = "badge-substitution" if algo["type"] == "Substitution" else "badge-transposition"
    sec_map = {"Low": "badge-low", "Medium": "badge-medium", "High*": "badge-high", "High": "badge-high"}
    sec_class = sec_map.get(algo["security"], "badge-medium")

    st.markdown(f"""
    <div class="cipher-header">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">
            <span style="font-size:2.5rem;">{algo["icon"]}</span>
            <div>
                <h1 style="margin:0 !important;font-size:1.8rem !important;">{algo["name"]}</h1>
                <div style="margin-top:0.3rem;">
                    <span class="badge {type_class}">{algo["type"]} Cipher</span>
                    &nbsp;
                    <span class="badge {sec_class}">Security: {algo["security"]}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown(f"### 📌 What is it?\n{algo['what']}")

        st.markdown("### ⚙️ How does it work?")
        for i, step in enumerate(algo["how"], 1):
            st.markdown(f"""
            <div style="display:flex;gap:0.75rem;margin-bottom:0.5rem;align-items:flex-start;">
                <div style="background:rgba(0,212,255,0.15);border:1px solid rgba(0,212,255,0.3);
                            border-radius:50%;width:24px;height:24px;display:flex;align-items:center;
                            justify-content:center;font-size:0.75rem;color:#00d4ff;font-weight:700;
                            flex-shrink:0;margin-top:0.1rem;">{i}</div>
                <div style="color:#e2e8f0;font-size:0.9rem;line-height:1.6;">{step}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"### 📥 Required Input\n{algo['input']}")
        st.markdown(f"### 🔑 Required Key\n{algo['key']}")

        st.markdown("### 📐 Formula / Rule")
        st.code(algo["formula"], language="text")

    with col_r:
        # Simple example box
        st.markdown("### 💡 Simple Example")
        ex = algo["example"]
        st.markdown(f"""
        <div class="crypto-card">
            <div style="margin-bottom:0.5rem;">
                <span style="color:#64748b;font-size:0.78rem;">PLAINTEXT</span><br>
                <code style="color:#e2e8f0;font-size:1rem;">{ex["plain"]}</code>
            </div>
            <div style="margin-bottom:0.5rem;">
                <span style="color:#64748b;font-size:0.78rem;">KEY</span><br>
                <code style="color:#a78bfa;font-size:1rem;">{ex["key"]}</code>
            </div>
            <div style="border-top:1px solid #1e3a5f;padding-top:0.5rem;margin-bottom:0.5rem;">
                <span style="color:#64748b;font-size:0.78rem;">CIPHERTEXT</span><br>
                <code style="color:#00d4ff;font-size:1rem;">{ex["cipher"]}</code>
            </div>
            <div>
                <span style="color:#64748b;font-size:0.78rem;">DECRYPTED</span><br>
                <code style="color:#10b981;font-size:1rem;">{ex["decrypt"]}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ✅ Advantages")
        for adv in algo["advantages"]:
            st.markdown(f"- ✅ {adv}")

        st.markdown("### ⚠️ Limitations")
        for lim in algo["limitations"]:
            st.markdown(f"- ❌ {lim}")

        st.markdown("### 🎯 Common Attacks")
        for att in algo["attacks"]:
            st.markdown(f"- 🔍 {att}")

    # Security level
    st.markdown("---")
    st.markdown("### 🔒 Security Level")
    sec_colors = {
        "Low": ("#ef4444", "🔴", "LOW — Easily broken by modern cryptanalysis."),
        "Medium": ("#f59e0b", "🟡", "MEDIUM (for classical ciphers) — Harder than simple ciphers but not secure by modern standards."),
        "High*": ("#10b981", "🟢", "HIGH* — Theoretically unbreakable when used correctly, but practical constraints limit real-world use."),
        "High": ("#10b981", "🟢", "HIGH — Theoretically unbreakable when used correctly."),
    }
    color, emoji, desc = sec_colors.get(algo["security"], ("#f59e0b", "🟡", ""))
    st.markdown(f"""
    <div style="background:rgba({
        '239,68,68' if algo['security']=='Low' else
        '245,158,11' if algo['security']=='Medium' else
        '16,185,129'
    },0.08);border:1px solid {color}40;border-left:3px solid {color};
                border-radius:0 8px 8px 0;padding:0.9rem 1.2rem;color:{color};">
        {emoji} <strong>{desc}</strong>
    </div>
    """, unsafe_allow_html=True)

