"""
Hill Cipher
===========
A polygraphic substitution cipher based on linear algebra.
This implementation supports a 2×2 key matrix.

Formula:
  Encrypt: C = (K × P) mod 26
  Decrypt: P = (K⁻¹ × C) mod 26

Where:
  K   = 2×2 key matrix
  K⁻¹ = modular inverse of K mod 26
  P   = column vector of plaintext letter indices
  C   = column vector of ciphertext letter indices

Requirements:
  - det(K) must be non-zero mod 26
  - gcd(det(K), 26) must equal 1 (i.e., det(K) must be coprime to 26)
  - Plaintext is padded with 'X' if length is odd.
"""

import time
import math
import numpy as np


# ────────────────────────── modular inverse helpers ──────────────────────────

def _mod_inverse(a: int, m: int) -> int:
    """
    Extended Euclidean Algorithm to find modular inverse of a mod m.
    Raises ValueError if the inverse does not exist.
    """
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Modular inverse of {a} mod {m} does not exist.")


def _matrix_mod_inverse(matrix: np.ndarray, mod: int) -> np.ndarray:
    """
    Compute the modular inverse of a 2×2 matrix mod `mod`.

    For 2×2 matrix [[a,b],[c,d]]:
      det = (a*d - b*c)
      adj = [[d, -b], [-c, a]]
      inv = det_inv * adj  (mod m)
    """
    det = int(round(np.linalg.det(matrix)))
    det_mod = det % mod
    det_inv = _mod_inverse(det_mod, mod)

    a, b = int(matrix[0, 0]), int(matrix[0, 1])
    c, d = int(matrix[1, 0]), int(matrix[1, 1])
    adjugate = np.array([[d, -b], [-c, a]])
    inv_matrix = (det_inv * adjugate) % mod
    return inv_matrix.astype(int)


# ──────────────────────────── validation ─────────────────────────────────────

def validate_matrix(matrix_values: list[int]) -> tuple[bool, str]:
    """
    Validate a 2×2 Hill Cipher key matrix.

    Args:
        matrix_values: List of 4 integers [a, b, c, d] (row-major order).

    Returns:
        (True, "") if valid
        (False, error_message) if invalid
    """
    if len(matrix_values) != 4:
        return False, "Exactly 4 values required for a 2×2 matrix."
    for v in matrix_values:
        if not isinstance(v, (int, np.integer)):
            return False, f"All matrix values must be integers. Got: {v}"
    matrix = np.array(matrix_values, dtype=int).reshape(2, 2)
    det = int(round(np.linalg.det(matrix))) % 26
    if det == 0:
        return False, "Matrix is not invertible mod 26 (determinant is 0 mod 26)."
    if math.gcd(det, 26) != 1:
        return False, (
            f"Determinant ({det % 26}) is not coprime with 26. "
            "Choose different matrix values."
        )
    return True, ""


# ─────────────────────────────── public API ───────────────────────────────────

def encrypt(text: str, matrix_values: list[int]) -> dict:
    """
    Encrypt plaintext using Hill Cipher (2×2 key matrix).

    Args:
        text: Input plaintext (non-alpha characters are removed).
        matrix_values: List of 4 integers for the 2×2 key matrix.

    Returns:
        dict with ciphertext, key_matrix, numeric_steps, time_taken
    """
    # Filter to alpha only, uppercase, pad with X if odd
    filtered = "".join(ch.upper() for ch in text if ch.isalpha())
    if len(filtered) % 2 != 0:
        filtered += "X"

    key_matrix = np.array(matrix_values, dtype=int).reshape(2, 2)
    numeric_steps = []  # List of (pair, plain_vec, cipher_vec)
    ciphertext_chars = []

    start = time.perf_counter()

    for i in range(0, len(filtered), 2):
        pair = filtered[i:i + 2]
        p_vec = np.array([ord(pair[0]) - ord('A'), ord(pair[1]) - ord('A')])
        c_vec = (key_matrix @ p_vec) % 26
        cipher_pair = chr(int(c_vec[0]) + ord('A')) + chr(int(c_vec[1]) + ord('A'))
        ciphertext_chars.append(cipher_pair)
        numeric_steps.append({
            "plain_pair": pair,
            "plain_vec": p_vec.tolist(),
            "cipher_vec": c_vec.tolist(),
            "cipher_pair": cipher_pair,
        })

    elapsed = time.perf_counter() - start

    return {
        "ciphertext": "".join(ciphertext_chars),
        "processed_plaintext": filtered,
        "key_matrix": key_matrix.tolist(),
        "numeric_steps": numeric_steps,
        "time_taken": elapsed,
    }


def decrypt(text: str, matrix_values: list[int]) -> dict:
    """
    Decrypt ciphertext using Hill Cipher.

    Args:
        text: Ciphertext to decrypt (non-alpha characters are removed).
        matrix_values: List of 4 integers for the 2×2 key matrix.

    Returns:
        dict with plaintext, inverse_matrix, numeric_steps, time_taken
    """
    filtered = "".join(ch.upper() for ch in text if ch.isalpha())
    if len(filtered) % 2 != 0:
        filtered += "X"

    key_matrix = np.array(matrix_values, dtype=int).reshape(2, 2)
    inv_matrix = _matrix_mod_inverse(key_matrix, 26)
    numeric_steps = []
    plaintext_chars = []

    start = time.perf_counter()

    for i in range(0, len(filtered), 2):
        pair = filtered[i:i + 2]
        c_vec = np.array([ord(pair[0]) - ord('A'), ord(pair[1]) - ord('A')])
        p_vec = (inv_matrix @ c_vec) % 26
        plain_pair = chr(int(p_vec[0]) + ord('A')) + chr(int(p_vec[1]) + ord('A'))
        plaintext_chars.append(plain_pair)
        numeric_steps.append({
            "cipher_pair": pair,
            "cipher_vec": c_vec.tolist(),
            "plain_vec": p_vec.tolist(),
            "plain_pair": plain_pair,
        })

    elapsed = time.perf_counter() - start

    return {
        "plaintext": "".join(plaintext_chars),
        "processed_ciphertext": filtered,
        "key_matrix": key_matrix.tolist(),
        "inverse_matrix": inv_matrix.tolist(),
        "numeric_steps": numeric_steps,
        "time_taken": elapsed,
    }
