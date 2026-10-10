"""
Caesar Cipher
=============
A substitution cipher that shifts each letter by a fixed number of positions
in the alphabet. Non-alphabetic characters are preserved unchanged.

Formula:
  Encrypt: C = (P + K) mod 26
  Decrypt: P = (C - K) mod 26
  where P = plaintext letter index (A=0), C = ciphertext letter index, K = shift key
"""

import time


def encrypt(text: str, shift: int) -> dict:
    """
    Encrypt plaintext using Caesar Cipher.

    Args:
        text: Input plaintext (any characters)
        shift: Integer shift key (any integer, applied mod 26)

    Returns:
        dict with keys: ciphertext, transformation_table, time_taken
    """
    shift = shift % 26
    ciphertext = []
    table = []  # List of (plain_char, shift, cipher_char) for alpha chars

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            encrypted_ch = chr((ord(ch) - base + shift) % 26 + base)
            ciphertext.append(encrypted_ch)
            table.append((ch.upper(), shift, encrypted_ch.upper()))
        else:
            ciphertext.append(ch)

    elapsed = time.perf_counter() - start

    return {
        "ciphertext": "".join(ciphertext),
        "transformation_table": table,
        "time_taken": elapsed,
    }


def decrypt(text: str, shift: int) -> dict:
    """
    Decrypt ciphertext using Caesar Cipher.

    Args:
        text: Ciphertext to decrypt
        shift: Integer shift key used during encryption

    Returns:
        dict with keys: plaintext, transformation_table, time_taken
    """
    shift = shift % 26
    plaintext = []
    table = []

    start = time.perf_counter()

    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            decrypted_ch = chr((ord(ch) - base - shift) % 26 + base)
            plaintext.append(decrypted_ch)
            table.append((ch.upper(), shift, decrypted_ch.upper()))
        else:
            plaintext.append(ch)

    elapsed = time.perf_counter() - start

    return {
        "plaintext": "".join(plaintext),
        "transformation_table": table,
        "time_taken": elapsed,
    }


def get_all_shifts_table(text: str) -> list:
    """
    Return a table showing the ciphertext for all 26 possible shifts.
    Useful for educational brute-force demonstration.

    Args:
        text: Ciphertext to try all shifts on

    Returns:
        List of (shift, decrypted_text) tuples
    """
    results = []
    for s in range(26):
        dec = decrypt(text, s)
        results.append((s, dec["plaintext"]))
    return results
