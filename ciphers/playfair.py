"""
Playfair Cipher
===============
A digraph substitution cipher that uses a 5×5 matrix built from a keyword.

Convention used in this implementation:
  - I and J are treated as the same letter (J → I).
  - The matrix contains 25 unique letters (A-Z excluding J).
  - Plaintext is split into digraphs (pairs of letters).
  - If a pair has identical letters, an 'X' is inserted between them.
  - If the total number of letters is odd, 'X' is appended.

Three Encryption Rules:
  1. Same Row    → shift each letter right (wrap around).
  2. Same Column → shift each letter down  (wrap around).
  3. Rectangle   → swap to opposite corners of the rectangle formed.

Decryption reverses the direction of shifts.
"""

import time


# ─────────────────────────── matrix helpers ──────────────────────────────────

def generate_matrix(keyword: str) -> list[list[str]]:
    """
    Build the 5×5 Playfair matrix from the given keyword.

    Args:
        keyword: Letters to seed the matrix (J treated as I).

    Returns:
        5×5 list of lists of characters.
    """
    keyword = keyword.upper().replace("J", "I")
    seen = set()
    sequence = []

    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            sequence.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # 25 letters, no J
        if ch not in seen:
            seen.add(ch)
            sequence.append(ch)

    matrix = [sequence[i * 5:(i + 1) * 5] for i in range(5)]
    return matrix


def _get_position(matrix: list[list[str]], ch: str) -> tuple[int, int]:
    """Return (row, col) of a character in the matrix."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == ch:
                return r, c
    raise ValueError(f"Character '{ch}' not found in matrix.")


# ──────────────────────────── preprocessing ──────────────────────────────────

def preprocess_plaintext(text: str) -> tuple[str, list[str]]:
    """
    Prepare plaintext for Playfair encryption.

    Steps:
      1. Keep only alphabetic characters, uppercase, J→I.
      2. Insert 'X' between repeated letters in a pair.
      3. Append 'X' if length is odd.

    Returns:
        (processed_string, list_of_digraphs)
    """
    # Step 1: filter and normalize
    filtered = ""
    for ch in text.upper():
        if ch.isalpha():
            filtered += "I" if ch == "J" else ch

    # Step 2: insert X between identical pair letters
    result = []
    i = 0
    while i < len(filtered):
        result.append(filtered[i])
        if i + 1 < len(filtered):
            if filtered[i] == filtered[i + 1]:
                result.append("X")
            else:
                result.append(filtered[i + 1])
                i += 1
        i += 1

    # Step 3: pad to even length
    if len(result) % 2 != 0:
        result.append("X")

    processed = "".join(result)
    digraphs = [processed[j:j + 2] for j in range(0, len(processed), 2)]
    return processed, digraphs


def _encrypt_digraph(matrix: list[list[str]], a: str, b: str) -> tuple[str, str]:
    """Apply Playfair encryption rule to a single digraph."""
    r1, c1 = _get_position(matrix, a)
    r2, c2 = _get_position(matrix, b)

    if r1 == r2:
        # Same row → shift right
        return matrix[r1][(c1 + 1) % 5], matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        # Same column → shift down
        return matrix[(r1 + 1) % 5][c1], matrix[(r2 + 1) % 5][c2]
    else:
        # Rectangle → swap columns
        return matrix[r1][c2], matrix[r2][c1]


def _decrypt_digraph(matrix: list[list[str]], a: str, b: str) -> tuple[str, str]:
    """Apply Playfair decryption rule to a single digraph."""
    r1, c1 = _get_position(matrix, a)
    r2, c2 = _get_position(matrix, b)

    if r1 == r2:
        # Same row → shift left
        return matrix[r1][(c1 - 1) % 5], matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        # Same column → shift up
        return matrix[(r1 - 1) % 5][c1], matrix[(r2 - 1) % 5][c2]
    else:
        # Rectangle → swap columns (same as encryption)
        return matrix[r1][c2], matrix[r2][c1]


# ─────────────────────────────── public API ───────────────────────────────────

def encrypt(text: str, keyword: str) -> dict:
    """
    Encrypt plaintext using Playfair Cipher.

    Args:
        text: Input plaintext
        keyword: Keyword for matrix generation

    Returns:
        dict with ciphertext, matrix, processed_text, digraphs, time_taken
    """
    matrix = generate_matrix(keyword)
    processed, digraphs = preprocess_plaintext(text)

    start = time.perf_counter()

    cipher_digraphs = []
    for dg in digraphs:
        ca, cb = _encrypt_digraph(matrix, dg[0], dg[1])
        cipher_digraphs.append(ca + cb)

    elapsed = time.perf_counter() - start

    ciphertext = "".join(cipher_digraphs)
    return {
        "ciphertext": ciphertext,
        "matrix": matrix,
        "processed_text": processed,
        "digraphs": digraphs,
        "cipher_digraphs": cipher_digraphs,
        "time_taken": elapsed,
    }


def decrypt(text: str, keyword: str) -> dict:
    """
    Decrypt ciphertext using Playfair Cipher.

    Args:
        text: Ciphertext (should contain only uppercase A-Z, excluding J, even length)
        keyword: Keyword used during encryption

    Returns:
        dict with plaintext, matrix, digraphs, time_taken
    """
    matrix = generate_matrix(keyword)
    # Normalize ciphertext: keep alpha, uppercase, J→I
    cleaned = "".join(
        ("I" if ch == "J" else ch)
        for ch in text.upper()
        if ch.isalpha()
    )

    if len(cleaned) % 2 != 0:
        cleaned += "X"  # safety pad

    digraphs = [cleaned[i:i + 2] for i in range(0, len(cleaned), 2)]

    start = time.perf_counter()

    plain_digraphs = []
    for dg in digraphs:
        pa, pb = _decrypt_digraph(matrix, dg[0], dg[1])
        plain_digraphs.append(pa + pb)

    elapsed = time.perf_counter() - start

    plaintext = "".join(plain_digraphs)
    return {
        "plaintext": plaintext,
        "matrix": matrix,
        "digraphs": digraphs,
        "plain_digraphs": plain_digraphs,
        "time_taken": elapsed,
    }
