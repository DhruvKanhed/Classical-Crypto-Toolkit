"""
Home / Dashboard Page
"""
import streamlit as st


ALGORITHMS = [
    {
        "name": "Caesar Cipher",
        "category": "Substitution",
        "description": "Shifts each letter by a fixed number of positions in the alphabet.",
        "security": "Low",
        "key": "Shift integer (0–25)",
        "icon": "🔡",
        "page": "Caesar Cipher",
    },
    {
        "name": "Monoalphabetic",
        "category": "Substitution",
        "description": "Maps each letter to a unique fixed substitute using a permutation key.",
        "security": "Low",
        "key": "26-character substitution alphabet",
        "icon": "🔤",
        "page": "Monoalphabetic Cipher",
    },
    {
        "name": "Playfair Cipher",
        "category": "Substitution",
        "description": "Encrypts digraphs (letter pairs) using a 5×5 keyword matrix.",
        "security": "Medium",
        "key": "Keyword (any word)",
        "icon": "🔲",
        "page": "Playfair Cipher",
    },
    {
        "name": "Hill Cipher",
        "category": "Substitution",
        "description": "Uses matrix multiplication mod 26 for polygraphic encryption.",
        "security": "Medium",
        "key": "2×2 invertible matrix (mod 26)",
        "icon": "🔢",
        "page": "Hill Cipher",
    },
    {
        "name": "Vigenère Cipher",
        "category": "Substitution",
        "description": "Applies multiple Caesar shifts using a repeating keyword.",
        "security": "Medium",
        "key": "Alphabetic keyword",
        "icon": "🗝️",
        "page": "Vigenère Cipher",
    },
    {
        "name": "One-Time Pad",
        "category": "Substitution",
        "description": "Theoretically unbreakable when the random key is used only once.",
        "security": "High*",
        "key": "Random key ≥ message length",
        "icon": "🛡️",
        "page": "One-Time Pad",
    },
    {
        "name": "Rail Fence Cipher",
        "category": "Transposition",
        "description": "Writes text in a zigzag pattern across multiple rails, then reads row-by-row.",
        "security": "Low",
        "key": "Number of rails (integer ≥ 2)",
        "icon": "🚂",
        "page": "Rail Fence Cipher",
    },
    {
        "name": "Columnar Transposition",
        "category": "Transposition",
        "description": "Rearranges letters in columns ordered by the alphabetical rank of the keyword.",
        "security": "Medium",
        "key": "Keyword (determines column order)",
        "icon": "📊",
        "page": "Columnar Transposition",
    },
]

SECURITY_COLOR = {
    "Low":    "badge-low",
    "Medium": "badge-medium",
    "High*":  "badge-high",
    "High":   "badge-high",
}


def render():
    # ── Hero Section ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1.5rem 0;">
        <div class="app-title">⚔️ Classical Cryptography Toolkit</div>
        <div class="app-subtitle" style="margin-top:0.5rem;">
            Explore &bull; Encrypt &bull; Decrypt &bull; Learn Classical Cryptography
        </div>
        <p style="color:#64748b; margin-top:0.75rem; font-size:0.92rem; max-width:600px; margin-left:auto; margin-right:auto;">
            An interactive educational toolkit demonstrating 8 classical encryption techniques.
            Built as a Final Year Network Security Mini Project.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat Cards (clickable) ────────────────────────────────────────────────
    NAV_TARGETS = {
        "Algorithms":      "Caesar Cipher",
        "Substitution":    "Caesar Cipher",
        "Transposition":   "Rail Fence Cipher",
        "Encrypt + Decrypt": "Caesar Cipher",
        "File Processing": "File Encryption",
        "Comparison":      "Compare Algorithms",
    }

    cols = st.columns(6)
    stats = [
        ("8",  "Algorithms"),
        ("6",  "Substitution"),
        ("2",  "Transposition"),
        ("🔐", "Encrypt + Decrypt"),
        ("📂", "File Processing"),
        ("📊", "Comparison"),
    ]
    for col, (num, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            target = NAV_TARGETS.get(label, "🏠 Home")
            btn_label = f"Open {label} ↗" if len(label) < 12 else "Open ↗"
            if st.button(btn_label, key=f"stat_{label}", use_container_width=True,
                         help=f"Navigate to {target}"):
                # push history
                history = st.session_state.get("nav_history", [])
                history.append(st.session_state.get("nav_page", "🏠 Home"))
                st.session_state["nav_history"] = history
                st.session_state["nav_page"] = target
                st.query_params["page"] = target
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CTA Buttons ───────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🔐 Start Encrypting", key="home_start", use_container_width=True):
            st.session_state["nav_page"] = "Caesar Cipher"
            st.query_params["page"] = "Caesar Cipher"
            st.rerun()
    with c2:
        if st.button("📖 Learn Cryptography", key="home_learn", use_container_width=True):
            st.session_state["nav_page"] = "Learn Algorithms"
            st.query_params["page"] = "Learn Algorithms"
            st.rerun()

    st.markdown("---")

    # ── Algorithm Cards ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>🗂️ Available Algorithms</h2>
    </div>
    """, unsafe_allow_html=True)

    # Render 4 per row
    for row_start in range(0, len(ALGORITHMS), 4):
        row_algos = ALGORITHMS[row_start:row_start + 4]
        cols = st.columns(len(row_algos))
        for col, algo in zip(cols, row_algos):
            with col:
                cat_class = "badge-substitution" if algo["category"] == "Substitution" else "badge-transposition"
                sec_class = SECURITY_COLOR.get(algo["security"], "badge-medium")
                st.markdown(f"""
                <div class="algo-card">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">{algo["icon"]}</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#e2e8f0; margin-bottom:0.4rem;">
                        {algo["name"]}
                    </div>
                    <div style="margin-bottom:0.6rem;">
                        <span class="badge {cat_class}">{algo["category"]}</span>
                        &nbsp;
                        <span class="badge {sec_class}">{algo["security"]}</span>
                    </div>
                    <div style="font-size:0.78rem; color:#94a3b8; margin-bottom:0.6rem; line-height:1.5;">
                        {algo["description"]}
                    </div>
                    <div style="font-size:0.72rem; color:#64748b;">
                        🔑 {algo["key"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open →", key=f"open_{algo['name']}", use_container_width=True):
                    st.session_state["nav_page"] = algo["page"]
                    st.query_params["page"] = algo["page"]
                    st.rerun()

    # ── Security Disclaimer ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Security Disclaimer:</strong> Classical ciphers (Caesar, Playfair, Hill, Vigenère, Rail Fence, etc.)
        are <em>not suitable</em> for protecting modern sensitive data. They are demonstrated here
        for educational purposes only. Do not use these for real-world security applications.
        Modern encryption algorithms such as AES, RSA, or ChaCha20 should be used instead.
    </div>
    """, unsafe_allow_html=True)

