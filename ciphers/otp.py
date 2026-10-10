"""
One-Time Pad (OTP) Cipher
==========================
Theoretically unbreakable cipher when used correctly.

Rules for a true OTP:
  1. The key must be truly random.
  2. The key must be at least as long as the message.
  3. The key must never be reused.
  4. The key must be kept completely secret.

⚠️  EDUCATIONAL DISCLAIMER:
This implementation is a DEMONSTRATION only. Python's random module is NOT
cryptographically secure. Do NOT use this for any real security purpose.
For real OTP-like security, use Python's secrets module or os.urandom().

Formula:
  Encrypt: C_i = (P_i + K_i) mod 26
  Decrypt: P_i = (C_i - K_i) mod 26

Only alphabetic characters are encrypted; others are passed through unchanged.
The key must have at least as many alphabetic characters as the plaintext.
"""

import random
import string
import time


def generate_key(text: str) -> str:
    """
    Generate a random key matching the number of alphabetic characters in text.

    Args:
        text: Plaintext (used only to determine key length).

    Returns:
        Random uppercase alphabetic key string.
    """
    alpha_count = sum(1 for ch in text if ch.isalpha())
    return "".join(random.choices(string.ascii_uppercase, k=alpha_count))


def validate_key(text: str, key: str) -> tuple[bool, str]:
    """
    Validate OTP key against the given text.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if not key:
        return False, "Key cannot be empty."
    key_clean = "".join(ch for ch in key.upper() if ch.isalpha())
    if not key_clean:
        return False, "Key must contain at least one alphabetic character."
    alpha_count = sum(1 for ch in text if ch.isalpha())
    if len(key_clean) < alpha_count:
        return False, (
            f"Key is too short. Need at least {alpha_count} alphabetic "
            f"characters, got {len(key_clean)}."
        )
    return True, ""


def encrypt(text: str, key: str) -> dict:
    """
    Encrypt plaintext using OTP.

    Args:
        text: Input plaintext
        key: Random key (≥ number of alphabetic chars in text)

    Returns:
        dict with ciphertext, key_used, char_table, time_taken
    """
    key_clean = "".join(ch.upper() for ch in key if ch.isalpha())
    ciphertext = []
    char_table = []
    key_idx = 0

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            k = ord(key_clean[key_idx]) - ord('A')
            enc = chr((ord(ch) - base + k) % 26 + base)
            ciphertext.append(enc)
            char_table.append((ch.upper(), key_clean[key_idx], k, enc.upper()))
            key_idx += 1
        else:
            ciphertext.append(ch)

    elapsed = time.perf_counter() - start

    return {
        "ciphertext": "".join(ciphertext),
        "key_used": key_clean[:key_idx],
        "char_table": char_table,
        "time_taken": elapsed,
    }


def decrypt(text: str, key: str) -> dict:
    """
    Decrypt ciphertext using OTP.

    Args:
        text: Ciphertext to decrypt
        key: The same key used for encryption

    Returns:
        dict with plaintext, key_used, char_table, time_taken
    """
    key_clean = "".join(ch.upper() for ch in key if ch.isalpha())
    plaintext = []
    char_table = []
    key_idx = 0

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            k = ord(key_clean[key_idx]) - ord('A')
            dec = chr((ord(ch) - base - k) % 26 + base)
            plaintext.append(dec)
            char_table.append((ch.upper(), key_clean[key_idx], k, dec.upper()))
            key_idx += 1
        else:
            plaintext.append(ch)

    elapsed = time.perf_counter() - start

    return {
        "plaintext": "".join(plaintext),
        "key_used": key_clean[:key_idx],
        "char_table": char_table,
        "time_taken": elapsed,
    }
