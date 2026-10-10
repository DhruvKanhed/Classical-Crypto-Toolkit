"""
Monoalphabetic Cipher
=====================
A substitution cipher where each letter of the alphabet is mapped to a unique
different letter using a fixed permutation (substitution alphabet / key).

Key:   Plain:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
       Cipher: Q W E R T Y U I O P A S D F G H J K L Z X C V B N M

Non-alphabetic characters are preserved unchanged.
"""

import random
import string
import time


# ─────────────────────────────── helpers ────────────────────────────────────

def generate_key() -> str:
    """Generate a random valid substitution alphabet (26 unique letters)."""
    alphabet = list(string.ascii_uppercase)
    random.shuffle(alphabet)
    return "".join(alphabet)


def validate_key(key: str) -> tuple[bool, str]:
    """
    Validate a monoalphabetic substitution key.

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if not key:
        return False, "Key cannot be empty."
    key_upper = key.upper().replace(" ", "")
    if len(key_upper) != 26:
        return False, f"Key must be exactly 26 characters long (got {len(key_upper)})."
    if not key_upper.isalpha():
        return False, "Key must contain only alphabetic characters."
    if len(set(key_upper)) != 26:
        return False, "Key must contain all 26 letters exactly once (no duplicates)."
    return True, ""


def _build_mapping(key: str) -> tuple[dict, dict]:
    """Build forward and reverse mapping dictionaries."""
    key_upper = key.upper()
    enc_map = {}
    dec_map = {}
    for i, plain_char in enumerate(string.ascii_uppercase):
        cipher_char = key_upper[i]
        enc_map[plain_char] = cipher_char
        dec_map[cipher_char] = plain_char
    return enc_map, dec_map


# ──────────────────────────── public API ────────────────────────────────────

def encrypt(text: str, key: str) -> dict:
    """
    Encrypt plaintext using Monoalphabetic Cipher.

    Args:
        text: Input plaintext
        key: 26-character substitution alphabet (uppercase or lowercase)

    Returns:
        dict with ciphertext, mapping_table, time_taken
    """
    enc_map, _ = _build_mapping(key)
    ciphertext = []
    mapping_table = []  # [(plain, cipher)] for alphabet display

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            upper_ch = ch.upper()
            encrypted = enc_map[upper_ch]
            # Preserve original case
            ciphertext.append(encrypted if ch.isupper() else encrypted.lower())
        else:
            ciphertext.append(ch)

    elapsed = time.perf_counter() - start

    # Build full alphabet → cipher mapping table for display
    for plain in string.ascii_uppercase:
        mapping_table.append((plain, enc_map[plain]))

    return {
        "ciphertext": "".join(ciphertext),
        "mapping_table": mapping_table,
        "time_taken": elapsed,
    }


def decrypt(text: str, key: str) -> dict:
    """
    Decrypt ciphertext using Monoalphabetic Cipher.

    Args:
        text: Ciphertext to decrypt
        key: The same 26-character substitution alphabet used for encryption

    Returns:
        dict with plaintext, mapping_table, time_taken
    """
    _, dec_map = _build_mapping(key)
    plaintext = []
    mapping_table = []

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            upper_ch = ch.upper()
            decrypted = dec_map.get(upper_ch, upper_ch)
            plaintext.append(decrypted if ch.isupper() else decrypted.lower())
        else:
            plaintext.append(ch)

    elapsed = time.perf_counter() - start

    enc_map, _ = _build_mapping(key)
    for plain in string.ascii_uppercase:
        mapping_table.append((plain, enc_map[plain]))

    return {
        "plaintext": "".join(plaintext),
        "mapping_table": mapping_table,
        "time_taken": elapsed,
    }
