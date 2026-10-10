"""
About Project Page
"""
import streamlit as st
from datetime import date


def render():
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem 0;">
        <div class="app-title" style="font-size:1.6rem;">ℹ️ About This Project</div>
        <p style="color:#94a3b8;margin-top:0.5rem;">
            Final Year Network Security Mini Project
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Project title card
    st.markdown("""
    <div class="cipher-header" style="text-align:center;">
        <div style="font-size:2.5rem;margin-bottom:0.5rem;">⚔️</div>
        <h1 style="font-size:1.8rem !important;margin-bottom:0.5rem !important;">
            Classical Cryptography Toolkit
        </h1>
        <p style="color:#94a3b8;font-size:0.95rem;margin-bottom:0.75rem;">
            Design and Development of a Classical Cryptography Toolkit
        </p>
        <div style="display:flex;justify-content:center;gap:0.75rem;flex-wrap:wrap;">
            <span class="badge badge-substitution">Network Security</span>
            <span class="badge badge-transposition">Mini Project</span>
            <span class="badge badge-high">Final Year</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Project Details ────────────────────────────────────────────────────────
    st.markdown("## 📋 Project Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎓 Student Information")

        # Editable fields
        student_name = st.text_input("Student Name", value="[Your Name]", key="about_name")
        roll_no = st.text_input("Roll Number", value="[Roll Number]", key="about_roll")
        batch = st.text_input("Batch", value="[Batch / Division]", key="about_batch")
        college = st.text_input("College Name", value="[College Name]", key="about_college")

        st.markdown("### 📅 Project Info")
        course = st.text_input("Course", value="Network Security", key="about_course")
        year = st.text_input("Academic Year", value="Final Year (ECM) – 2026-27", key="about_year")
        project_date = st.date_input("Date", value=date.today(), key="about_date")

    with col2:
        st.markdown("### 🎯 Objective")
        st.markdown("""
        <div class="crypto-card">
            To design and develop an interactive software application that implements classical
            cryptography algorithms for text encryption, decryption, comparison, and educational
            demonstration.<br><br>
            The toolkit serves as both a <strong>working cryptography tool</strong> and an
            <strong>educational learning platform</strong> for students studying Network Security.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Project Scope")
        features = [
            "8 classical encryption algorithms",
            "Encryption + decryption for all algorithms",
            "Interactive educational content",
            "Algorithm comparison tool",
            "File encryption/decryption",
            "Execution time measurement",
            "Step-by-step working display",
            "Download results as .txt files",
        ]
        for f in features:
            st.markdown(f"- ✅ {f}")

    st.markdown("---")

    # ── Technology Stack ────────────────────────────────────────────────────────
    st.markdown("## 🛠️ Technology Stack")
    col1, col2, col3, col4 = st.columns(4)
    tech = [
        ("🐍", "Python 3.x", "Core programming language"),
        ("🌊", "Streamlit", "Web application framework"),
        ("🔢", "NumPy", "Hill Cipher matrix operations"),
        ("📊", "Pandas", "Data tables and comparison"),
    ]
    for col, (icon, name, desc) in zip([col1, col2, col3, col4], tech):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="text-align:center;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:700;color:#e2e8f0;margin:0.3rem 0;">{name}</div>
                <div style="color:#94a3b8;font-size:0.78rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Algorithms Implemented ───────────────────────────────────────────────
    st.markdown("## 🔐 Algorithms Implemented")
    algo_info = [
        ("Substitution Ciphers", [
            ("🔡", "Caesar Cipher", "Classic shift cipher"),
            ("🔤", "Monoalphabetic Cipher", "Fixed permutation substitution"),
            ("🔲", "Playfair Cipher", "Digraph substitution with 5×5 matrix"),
            ("🔢", "Hill Cipher", "Matrix multiplication mod 26"),
            ("🗝️", "Vigenère Cipher", "Polyalphabetic repeating-key cipher"),
            ("🛡️", "One-Time Pad", "Theoretically unbreakable cipher"),
        ]),
        ("Transposition Ciphers", [
            ("🚂", "Rail Fence Cipher", "Zigzag transposition"),
            ("📊", "Columnar Transposition", "Column-reordering transposition"),
        ]),
    ]

    for category, algos in algo_info:
        st.markdown(f"### {category}")
        cols = st.columns(min(len(algos), 3))
        for col, (icon, name, desc) in zip(cols * 3, algos):
            with col:
                st.markdown(f"""
                <div class="algo-card" style="margin-bottom:0.5rem;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div style="font-weight:700;color:#e2e8f0;font-size:0.9rem;margin:0.3rem 0;">{name}</div>
                    <div style="color:#94a3b8;font-size:0.78rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Security Disclaimer ───────────────────────────────────────────────────
    st.markdown("## ⚠️ Security Disclaimer")
    st.markdown("""
    <div class="warning-box">
        <strong>This application is an educational classical cryptography toolkit.</strong><br><br>
        Classical ciphers such as Caesar, Playfair, Hill, Vigenère, Rail Fence, Columnar Transposition,
        and Monoalphabetic ciphers are <strong>not appropriate for protecting modern sensitive data</strong>.
        They were developed centuries ago and can be broken with modern techniques such as:
        frequency analysis, known-plaintext attacks, and computational brute force.<br><br>
        For real-world security applications, use modern cryptographic standards such as:
        <strong>AES-256</strong>, <strong>RSA</strong>, <strong>ChaCha20-Poly1305</strong>,
        or <strong>Elliptic Curve Cryptography (ECC)</strong>.<br><br>
        The One-Time Pad (OTP) implementation here uses Python's <code>random</code> module
        which is NOT cryptographically secure. A true OTP requires a hardware random number generator.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#64748b;font-size:0.8rem;padding:1rem 0;">
        Built with ❤️ using Python & Streamlit | Classical Cryptography Toolkit
    </div>
    """, unsafe_allow_html=True)

