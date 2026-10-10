"""
Validators
==========
Centralized input validation functions for all cipher pages.
Each function returns (is_valid: bool, error_message: str).
"""

import string
import math


def validate_caesar_key(key_str: str) -> tuple[bool, str]:
    """Validate Caesar Cipher shift key."""
    try:
        int(key_str)
        return True, ""
    except (ValueError, TypeError):
        return False, "Shift key must be a valid integer (e.g., 3, -5, 13)."


def validate_mono_key(key: str) -> tuple[bool, str]:
    """Validate Monoalphabetic substitution key."""
    if not key:
        return False, "Key cannot be empty."
    key_upper = key.upper().replace(" ", "")
    if len(key_upper) != 26:
        return False, f"Key must be exactly 26 characters (got {len(key_upper)})."
    if not key_upper.isalpha():
        return False, "Key must contain only alphabetic characters."
    if len(set(key_upper)) != 26:
        return False, "Key must contain all 26 letters exactly once (no repeats)."
    return True, ""


def validate_playfair_key(keyword: str) -> tuple[bool, str]:
    """Validate Playfair Cipher keyword."""
    if not keyword or not keyword.strip():
        return False, "Keyword cannot be empty."
    if not all(ch.isalpha() or ch.isspace() for ch in keyword):
        return False, "Keyword must contain only alphabetic characters."
    alpha_only = "".join(ch for ch in keyword if ch.isalpha())
    if len(alpha_only) == 0:
        return False, "Keyword must contain at least one letter."
    return True, ""


def validate_hill_matrix(values: list) -> tuple[bool, str]:
    """Validate Hill Cipher 2×2 key matrix."""
    if len(values) != 4:
        return False, "Exactly 4 values are required for a 2×2 matrix."
    for i, v in enumerate(values):
        try:
            int(v)
        except (ValueError, TypeError):
            return False, f"Matrix value {i+1} must be a valid integer."

    int_vals = [int(v) for v in values]
    a, b, c, d = int_vals
    det = (a * d - b * c) % 26
    if det == 0:
        return False, (
            f"The matrix determinant is 0 (mod 26). "
            "This matrix is not invertible and cannot be used for Hill Cipher. "
            "Try different values."
        )
    if math.gcd(det, 26) != 1:
        return False, (
            f"The determinant ({det}) is not coprime with 26 (gcd={math.gcd(det,26)}). "
            "The matrix must have gcd(det, 26) = 1. Try different values."
        )
    return True, ""


def validate_vigenere_key(keyword: str) -> tuple[bool, str]:
    """Validate Vigenère Cipher keyword."""
    if not keyword or not keyword.strip():
        return False, "Keyword cannot be empty."
    alpha_only = "".join(ch for ch in keyword if ch.isalpha())
    if len(alpha_only) == 0:
        return False, "Keyword must contain at least one alphabetic character."
    return True, ""


def validate_otp_key(text: str, key: str) -> tuple[bool, str]:
    """Validate One-Time Pad key against plaintext."""
    if not key:
        return False, "Key cannot be empty."
    key_alpha = "".join(ch for ch in key if ch.isalpha())
    if not key_alpha:
        return False, "Key must contain at least one alphabetic character."
    text_alpha_count = sum(1 for ch in text if ch.isalpha())
    if len(key_alpha) < text_alpha_count:
        return False, (
            f"Key is too short. The plaintext has {text_alpha_count} alphabetic "
            f"characters but the key only has {len(key_alpha)}. "
            "Generate a new key or provide a longer one."
        )
    return True, ""


def validate_rail_fence_key(rails_str: str, text: str = "") -> tuple[bool, str]:
    """Validate Rail Fence number of rails."""
    try:
        rails = int(rails_str)
    except (ValueError, TypeError):
        return False, "Number of rails must be a valid integer."
    if rails < 2:
        return False, "Number of rails must be at least 2."
    if text and rails >= len(text):
        return False, (
            f"Number of rails ({rails}) must be less than the text length "
            f"({len(text)}) for meaningful transposition."
        )
    return True, ""


def validate_columnar_key(keyword: str) -> tuple[bool, str]:
    """Validate Columnar Transposition keyword."""
    if not keyword or not keyword.strip():
        return False, "Keyword cannot be empty."
    return True, ""


def validate_columnar_params(text: str, rows: int, cols: int, key: str, mode: str = "encrypt") -> tuple[bool, str]:
    """Validate Columnar Transposition parameter combination matching the Colab notebook logic."""
    if cols <= 0:
        return False, "Number of columns must be a positive integer."
    if not key or not key.strip():
        return False, "Key cannot be empty."
    if not key.isdigit():
        return False, "Key must be numeric (e.g., 43125)."
    if len(key) != cols:
        return False, f"Key length must be equal to the number of columns ({cols})."

    # For encrypt: ensure grid is large enough
    if mode == "encrypt":
        processed_text = "".join(ch for ch in text if not ch.isspace())
        if rows <= 0:
            return False, "Number of rows must be a positive integer."
        if len(processed_text) > rows * cols:
            return False, f"Matrix size is too small. Plaintext has {len(processed_text)} characters, but grid only has space for {rows * cols}."

    # Decrypt: no length check — rows are calculated automatically from ciphertext length
    return True, ""


def validate_text_not_empty(text: str, field_name: str = "Text") -> tuple[bool, str]:
    """Generic check that text is not empty."""
    if not text or not text.strip():
        return False, f"{field_name} cannot be empty."
    return True, ""
