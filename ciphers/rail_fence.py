"""
Rail Fence Cipher
=================
A transposition cipher that writes the plaintext in a zigzag pattern
across a number of "rails" (rows), then reads off each rail in order.

Example with 3 rails and text "WEAREDISCOVEREDFLEEATONCE":
  Rail 0: W . . . E . . . I . . . V . . . D . . . E . . . C .
  Rail 1: . E . R . D . S . O . E . E . F . E . A . O . C .
  Rail 2: . . A . . . . . C . . . R . . . L . . . T . . . N . E

Ciphertext is formed by concatenating each rail left-to-right:
  Rail 0: WEIDEC
  Rail 1: ERDSOEEFEAOC
  Rail 2: ACRLTNE
  → WEIDECERDSOEEFEA OCACRLTNE

Non-alphabetic characters are included in the zigzag as-is.
"""

import time


def _build_rail_grid(text: str, rails: int) -> list[list[str]]:
    """
    Build the zigzag grid.

    Returns a list of `rails` lists, each containing the characters
    that fall on that rail (in left-to-right order).
    """
    grid = [[] for _ in range(rails)]
    rail = 0
    direction = 1  # 1 = going down, -1 = going up

    for ch in text:
        grid[rail].append(ch)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    return grid


def _build_full_grid(text: str, rails: int) -> list[list[str]]:
    """
    Build a 2D grid (rails × len(text)) for visual display.
    Empty cells are represented by '.'.
    """
    grid = [['.' for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    direction = 1

    for col, ch in enumerate(text):
        grid[rail][col] = ch
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    return grid


def encrypt(text: str, rails: int) -> dict:
    """
    Encrypt text using Rail Fence Cipher.

    Args:
        text: Input plaintext (any characters)
        rails: Number of rails (must be ≥ 2)

    Returns:
        dict with ciphertext, rail_strings, visual_grid, time_taken
    """
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")
    if rails >= len(text):
        # With rails ≥ length, cipher = plaintext (no transposition effect)
        return {
            "ciphertext": text,
            "rail_strings": [text[i:i+1] if i < len(text) else "" for i in range(rails)],
            "visual_grid": _build_full_grid(text, rails),
            "time_taken": 0.0,
        }

    start = time.perf_counter()

    rail_grid = _build_rail_grid(text, rails)
    ciphertext = "".join("".join(rail) for rail in rail_grid)
    visual_grid = _build_full_grid(text, rails)

    elapsed = time.perf_counter() - start

    return {
        "ciphertext": ciphertext,
        "rail_strings": ["".join(r) for r in rail_grid],
        "visual_grid": visual_grid,
        "time_taken": elapsed,
    }


def decrypt(text: str, rails: int) -> dict:
    """
    Decrypt ciphertext using Rail Fence Cipher.

    Args:
        text: Ciphertext to decrypt
        rails: Number of rails used during encryption

    Returns:
        dict with plaintext, time_taken
    """
    if rails < 2:
        raise ValueError("Number of rails must be at least 2.")
    if rails >= len(text):
        return {"plaintext": text, "time_taken": 0.0}

    n = len(text)
    # Determine which rail each position belongs to
    pattern = []
    rail = 0
    direction = 1
    for _ in range(n):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    # Count characters per rail
    rail_lengths = [0] * rails
    for r in pattern:
        rail_lengths[r] += 1

    # Split ciphertext into rails
    rails_data = []
    idx = 0
    for length in rail_lengths:
        rails_data.append(list(text[idx:idx + length]))
        idx += length

    # Read off in original order
    start = time.perf_counter()

    rail_indices = [0] * rails
    plaintext = []
    for r in pattern:
        plaintext.append(rails_data[r][rail_indices[r]])
        rail_indices[r] += 1

    elapsed = time.perf_counter() - start

    return {
        "plaintext": "".join(plaintext),
        "time_taken": elapsed,
    }
