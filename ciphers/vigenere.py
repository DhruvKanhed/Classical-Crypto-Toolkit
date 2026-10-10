"""
Vigenère (Polyalphabetic) Cipher
=================================
Uses a repeating keyword to apply multiple Caesar shifts.
Each letter of the keyword determines the shift for the corresponding
plaintext letter.

Formula:
  Encrypt: C_i = (P_i + K_i) mod 26
  Decrypt: P_i = (C_i - K_i) mod 26

Where K_i is the i-th letter of the repeated keyword (A=0, B=1, …, Z=25).

Non-alphabetic characters are preserved without consuming a key character.
"""

import time


def _repeat_key(text: str, keyword: str) -> str:
    """
    Extend the keyword to match the number of alphabetic characters in text.
    Non-alpha characters in text do not consume keyword characters.
    """
    keyword = keyword.upper()
    key_stream = []
    key_idx = 0
    for ch in text:
        if ch.isalpha():
            key_stream.append(keyword[key_idx % len(keyword)])
            key_idx += 1
        else:
            key_stream.append(None)  # placeholder for non-alpha
    return key_stream


def encrypt(text: str, keyword: str) -> dict:
    """
    Encrypt plaintext using Vigenère Cipher.

    Args:
        text: Input plaintext
        keyword: Alphabetic keyword (any length ≥ 1)

    Returns:
        dict with ciphertext, key_stream, char_table, time_taken
    """
    keyword = keyword.upper()
    key_stream = _repeat_key(text, keyword)
    ciphertext = []
    char_table = []  # [(plain, key_char, shift, cipher)] for alpha chars

    start = time.perf_counter()

    for ch, k in zip(text, key_stream):
        if ch.isalpha() and k is not None:
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(k) - ord('A')
            enc = chr((ord(ch) - base + shift) % 26 + base)
            ciphertext.append(enc)
            char_table.append((ch.upper(), k, shift, enc.upper()))
        else:
            ciphertext.append(ch)

    elapsed = time.perf_counter() - start

    # Build only alpha key stream for display
    alpha_key = [k for k in key_stream if k is not None]

    return {
        "ciphertext": "".join(ciphertext),
        "key_stream": "".join(alpha_key),
        "char_table": char_table,
        "time_taken": elapsed,
    }


def decrypt(text: str, keyword: str) -> dict:
    """
    Decrypt ciphertext using Vigenère Cipher.

    Args:
        text: Ciphertext to decrypt
        keyword: Alphabetic keyword used during encryption

    Returns:
        dict with plaintext, key_stream, char_table, time_taken
    """
    keyword = keyword.upper()
    key_stream = _repeat_key(text, keyword)
    plaintext = []
    char_table = []

    start = time.perf_counter()

    for ch, k in zip(text, key_stream):
        if ch.isalpha() and k is not None:
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(k) - ord('A')
            dec = chr((ord(ch) - base - shift) % 26 + base)
            plaintext.append(dec)
            char_table.append((ch.upper(), k, shift, dec.upper()))
        else:
            plaintext.append(ch)

    elapsed = time.perf_counter() - start

    alpha_key = [k for k in key_stream if k is not None]

    return {
        "plaintext": "".join(plaintext),
        "key_stream": "".join(alpha_key),
        "char_table": char_table,
        "time_taken": elapsed,
    }
