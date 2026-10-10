"""
Columnar Transposition Cipher (Row-Column specific logic)
==========================================================
A transposition cipher that arranges plaintext in a grid of specified rows and columns,
then reads the columns in order determined by the key.
"""

import time

def encrypt(text: str, rows: int, cols: int, key: str) -> dict:
    """
    Encrypt plaintext using Columnar Transposition with specified rows, cols, and key.
    """
    start = time.perf_counter()
    
    # Preprocess text: uppercase and remove spaces to match Colab implementation
    processed_text = "".join(ch.upper() for ch in text if not ch.isspace())
    
    # Pad plaintext with 'X' to rows * cols
    padded_text = processed_text
    while len(padded_text) < rows * cols:
        padded_text += 'X'
        
    # Build grid
    grid = []
    k = 0
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(padded_text[k])
            k += 1
        grid.append(row)
        
    # Determine reading order
    column_order = sorted(range(len(key)), key=lambda x: key[x])
    
    # Read columns in key order
    cipher = ""
    for col in column_order:
        for row in range(rows):
            cipher += grid[row][col]
            
    elapsed = time.perf_counter() - start
    
    return {
        "ciphertext": cipher,
        "grid": grid,
        "column_order": column_order,
        "padded_text": padded_text,
        "num_rows": rows,
        "num_cols": cols,
        "keyword": key,
        "time_taken": elapsed
    }

def decrypt(cipher: str, rows: int, cols: int, key: str) -> dict:
    """
    Decrypt ciphertext using Columnar Transposition with specified rows, cols, and key.
    """
    start = time.perf_counter()
    
    # Preprocess cipher: uppercase and remove spaces
    processed_cipher = "".join(ch.upper() for ch in cipher if not ch.isspace())
    
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    column_order = sorted(range(len(key)), key=lambda x: key[x])
    
    k = 0
    for col in column_order:
        for row in range(rows):
            # Safe index access check
            if k < len(processed_cipher):
                grid[row][col] = processed_cipher[k]
            else:
                grid[row][col] = 'X'
            k += 1
            
    plaintext = ""
    for row in range(rows):
        for col in range(cols):
            plaintext += grid[row][col]
            
    # Strip trailing X padding
    plaintext_stripped = plaintext.rstrip('X')
    
    elapsed = time.perf_counter() - start
    
    return {
        "plaintext": plaintext_stripped,
        "grid": grid,
        "column_order": column_order,
        "time_taken": elapsed
    }
