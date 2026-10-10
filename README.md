# Classical Cryptography Toolkit

> **Final Year Network Security Mini Project**
> Design and Development of a Classical Cryptography Toolkit

---

## Overview

An interactive, educational web application demonstrating **8 classical cryptography algorithms** — built using Python and Streamlit. The application serves as both a working cryptography toolkit and an educational learning platform.

## Features

- ✅ **8 Classical Ciphers** — All with encryption + decryption
- 📖 **Educational Content** — Student-friendly explanations for all algorithms
- 📊 **Algorithm Comparison** — Side-by-side comparison table + interactive runner
- 📂 **File Encryption** — Upload `.txt` files, encrypt/decrypt, and download results
- ⏱️ **Execution Time** — Measured for every operation
- 🔍 **Step-by-step Working** — Character transformation tables, digraph tables, matrix steps
- 🌙 **Dark Cybersecurity Theme** — Modern, premium UI

## Algorithms Implemented

### Substitution Ciphers
| Algorithm | Key | Description |
|-----------|-----|-------------|
| Caesar Cipher | Integer shift (0–25) | Shifts each letter by a fixed number |
| Monoalphabetic | 26-letter permutation | Fixed substitution table |
| Playfair Cipher | Keyword → 5×5 matrix | Digraph substitution |
| Hill Cipher | 2×2 invertible matrix | Matrix multiplication mod 26 |
| Vigenère Cipher | Alphabetic keyword | Polyalphabetic repeating shifts |
| One-Time Pad | Random key ≥ msg length | Vernam cipher (educational demo) |

### Transposition Ciphers
| Algorithm | Key | Description |
|-----------|-----|-------------|
| Rail Fence Cipher | Number of rails | Zigzag rearrangement |
| Columnar Transposition | Keyword | Column-based rearrangement |

## Project Structure

```
NS_project/
│
├── app.py                      # Main Streamlit application
├── requirements.txt
├── README.md
│
├── ciphers/                    # Cipher logic (no UI)
│   ├── __init__.py
│   ├── caesar.py
│   ├── monoalphabetic.py
│   ├── playfair.py
│   ├── hill.py
│   ├── vigenere.py
│   ├── otp.py
│   ├── rail_fence.py
│   └── columnar.py
│
├── utils/                      # Utility helpers
│   ├── __init__.py
│   ├── validators.py
│   ├── timing.py
│   └── file_handler.py
│
├── pages/                      # Streamlit UI pages
│   ├── __init__.py
│   ├── home.py
│   ├── ui_helpers.py
│   ├── caesar_page.py
│   ├── monoalphabetic_page.py
│   ├── playfair_page.py
│   ├── hill_page.py
│   ├── vigenere_page.py
│   ├── otp_page.py
│   ├── rail_fence_page.py
│   ├── columnar_page.py
│   ├── learn_page.py
│   ├── compare_page.py
│   ├── file_page.py
│   ├── help_page.py
│   └── about_page.py
│
├── assets/
│   └── styles.css              # Custom dark theme CSS
│
└── tests/
    └── test_ciphers.py         # Unit tests for all ciphers
```

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# Clone or download the project
# Navigate to the project directory
cd NS_project

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Running Tests

```bash
python -m pytest tests/test_ciphers.py -v
```

## Usage

1. **Navigate** using the sidebar to select any cipher or section
2. **Enter** your plaintext or ciphertext in the input field
3. **Enter or generate** the required key
4. **Click** Encrypt or Decrypt
5. **View** the result table and step-by-step working
6. **Download** the result if needed

## Known Test Vectors

| Algorithm | Plaintext | Key | Expected Ciphertext |
|-----------|-----------|-----|-------------------|
| Caesar | HELLO | 3 | KHOOR |
| Vigenère | ATTACKATDAWN | LEMON | LXFOPVEFRNHR |
| Caesar | PYTHON | 13 | CLGUBA |

## Security Disclaimer

> ⚠️ This application is for **educational purposes only**. Classical ciphers are NOT secure for modern use. For real-world applications, use AES, RSA, ChaCha20, or other modern algorithms.

## Technologies Used

- **Python 3.x** — Core logic
- **Streamlit** — Web application framework
- **NumPy** — Hill Cipher matrix operations
- **Pandas** — Data tables and comparison views

---

*Final Year Network Security Mini Project — 2026-27*
