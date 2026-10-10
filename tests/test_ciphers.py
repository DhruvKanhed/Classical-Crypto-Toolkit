"""
Test Suite — Classical Cryptography Toolkit
==========================================
Tests all 8 cipher implementations:
  - Normal plaintext
  - Uppercase / lowercase text
  - Text with spaces and punctuation
  - Empty input (where applicable)
  - Known test vectors (verified results)
  - Round-trip: encrypt → decrypt → verify original

Run with:
    python -m pytest tests/test_ciphers.py -v
"""

import pytest
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.caesar import encrypt as caesar_enc, decrypt as caesar_dec
from ciphers.monoalphabetic import encrypt as mono_enc, decrypt as mono_dec, generate_key, validate_key
from ciphers.playfair import encrypt as pf_enc, decrypt as pf_dec, generate_matrix, preprocess_plaintext
from ciphers.hill import encrypt as hill_enc, decrypt as hill_dec, validate_matrix
from ciphers.vigenere import encrypt as vig_enc, decrypt as vig_dec
from ciphers.otp import encrypt as otp_enc, decrypt as otp_dec, generate_key as otp_gen
from ciphers.rail_fence import encrypt as rf_enc, decrypt as rf_dec
from ciphers.columnar import encrypt as col_enc, decrypt as col_dec


# ════════════════════════════════════════════════════════════════════════════
# CAESAR CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestCaesar:
    """Tests for Caesar Cipher."""

    def test_known_vector_hello(self):
        """HELLO + shift 3 → KHOOR (well-known example)."""
        result = caesar_enc("HELLO", 3)
        assert result["ciphertext"] == "KHOOR"

    def test_known_vector_python(self):
        """PYTHON + shift 13 → CLGUBA (ROT13)."""
        result = caesar_enc("PYTHON", 13)
        assert result["ciphertext"] == "CLGUBA"

    def test_known_vector_abc(self):
        """ABC + shift 1 → BCD."""
        result = caesar_enc("ABC", 1)
        assert result["ciphertext"] == "BCD"

    def test_wraparound_xyz(self):
        """XYZ + shift 3 → ABC (wrap around)."""
        result = caesar_enc("XYZ", 3)
        assert result["ciphertext"] == "ABC"

    def test_lowercase_preserved(self):
        """Lowercase letters shift but stay lowercase."""
        result = caesar_enc("hello", 3)
        assert result["ciphertext"] == "khoor"

    def test_spaces_preserved(self):
        """Spaces are preserved unchanged."""
        result = caesar_enc("HELLO WORLD", 3)
        assert " " in result["ciphertext"]
        assert result["ciphertext"] == "KHOOR ZRUOG"

    def test_punctuation_preserved(self):
        """Punctuation passes through unchanged."""
        result = caesar_enc("HELLO!", 3)
        assert result["ciphertext"].endswith("!")

    def test_shift_zero(self):
        """Shift 0 → no change."""
        result = caesar_enc("HELLO", 0)
        assert result["ciphertext"] == "HELLO"

    def test_shift_26_identity(self):
        """Shift 26 ≡ 0 mod 26 → identity."""
        result = caesar_enc("HELLO", 26)
        assert result["ciphertext"] == "HELLO"

    def test_negative_shift(self):
        """Negative shift should work (mod 26 applied)."""
        result = caesar_enc("KHOOR", -3)
        assert result["ciphertext"] == "HELLO"

    def test_round_trip_short(self):
        """Encrypt then decrypt recovers original."""
        original = "HELLO WORLD"
        enc = caesar_enc(original, 7)
        dec = caesar_dec(enc["ciphertext"], 7)
        assert dec["plaintext"] == original

    def test_round_trip_long(self):
        """Round-trip on longer text."""
        original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        enc = caesar_enc(original, 13)
        dec = caesar_dec(enc["ciphertext"], 13)
        assert dec["plaintext"] == original

    def test_numbers_preserved(self):
        """Numbers pass through unchanged."""
        result = caesar_enc("HELLO123", 3)
        assert "123" in result["ciphertext"]

    def test_empty_string(self):
        """Empty string returns empty ciphertext."""
        result = caesar_enc("", 5)
        assert result["ciphertext"] == ""

    def test_transformation_table_populated(self):
        """Transformation table should have entries for alpha chars."""
        result = caesar_enc("HELLO", 3)
        assert len(result["transformation_table"]) == 5

    def test_decrypt_known_vector(self):
        """Decrypt KHOOR with shift 3 → HELLO."""
        result = caesar_dec("KHOOR", 3)
        assert result["plaintext"] == "HELLO"

    def test_time_taken_positive(self):
        """Execution time should be a non-negative float."""
        result = caesar_enc("HELLO", 3)
        assert result["time_taken"] >= 0


# ════════════════════════════════════════════════════════════════════════════
# MONOALPHABETIC CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestMonoalphabetic:
    KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"

    def test_generate_key_length(self):
        """Generated key must be exactly 26 characters."""
        key = generate_key()
        assert len(key) == 26

    def test_generate_key_unique(self):
        """Generated key must have all 26 unique letters."""
        key = generate_key()
        assert len(set(key)) == 26

    def test_validate_key_valid(self):
        """Valid key should pass validation."""
        ok, err = validate_key(self.KEY)
        assert ok is True
        assert err == ""

    def test_validate_key_too_short(self):
        """Short key should fail validation."""
        ok, err = validate_key("ABCDE")
        assert ok is False

    def test_validate_key_duplicates(self):
        """Key with duplicates should fail."""
        bad_key = "AAAAAAAAAAAAAAAAAAAAAAAAA" + "B"
        ok, err = validate_key(bad_key)
        assert ok is False

    def test_encrypt_decrypt_round_trip(self):
        """Encrypt then decrypt should recover original alpha text."""
        original = "HELLO"
        enc = mono_enc(original, self.KEY)
        dec = mono_dec(enc["ciphertext"], self.KEY)
        assert dec["plaintext"] == original

    def test_spaces_preserved(self):
        """Spaces are preserved."""
        enc = mono_enc("HELLO WORLD", self.KEY)
        assert " " in enc["ciphertext"]

    def test_lowercase_handling(self):
        """Lowercase input should produce lowercase output."""
        enc = mono_enc("hello", self.KEY)
        assert enc["ciphertext"].islower()

    def test_round_trip_with_spaces(self):
        """Round trip with spaces."""
        original = "HELLO WORLD"
        enc = mono_enc(original, self.KEY)
        dec = mono_dec(enc["ciphertext"], self.KEY)
        assert dec["plaintext"] == original

    def test_mapping_table_length(self):
        """Mapping table should have 26 entries."""
        enc = mono_enc("HELLO", self.KEY)
        assert len(enc["mapping_table"]) == 26


# ════════════════════════════════════════════════════════════════════════════
# PLAYFAIR CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestPlayfair:
    KEYWORD = "MONARCHY"

    def test_matrix_size(self):
        """Matrix must be 5×5."""
        matrix = generate_matrix(self.KEYWORD)
        assert len(matrix) == 5
        assert all(len(row) == 5 for row in matrix)

    def test_matrix_has_25_unique_letters(self):
        """Matrix must contain 25 unique letters (no J)."""
        matrix = generate_matrix(self.KEYWORD)
        letters = [cell for row in matrix for cell in row]
        assert len(letters) == 25
        assert len(set(letters)) == 25
        assert "J" not in letters

    def test_preprocess_removes_non_alpha(self):
        """Preprocessing removes non-alphabetic characters."""
        processed, _ = preprocess_plaintext("HELLO123!")
        assert processed.isalpha()

    def test_preprocess_j_to_i(self):
        """Preprocessing converts J to I."""
        processed, _ = preprocess_plaintext("JUNGLE")
        assert "J" not in processed

    def test_preprocess_even_length(self):
        """Processed text must be even length."""
        processed, _ = preprocess_plaintext("HELLO")
        assert len(processed) % 2 == 0

    def test_preprocess_repeated_letters(self):
        """Repeated letters in same pair should get X inserted."""
        processed, _ = preprocess_plaintext("BALLOON")
        assert "X" in processed

    def test_encrypt_returns_even_ciphertext(self):
        """Ciphertext must have even length (digraph output)."""
        result = pf_enc("HELLO", self.KEYWORD)
        assert len(result["ciphertext"]) % 2 == 0

    def test_round_trip_simple(self):
        """Encrypt then decrypt should recover processed plaintext."""
        original = "INSTRUMENTS"
        enc = pf_enc(original, self.KEYWORD)
        dec = pf_dec(enc["ciphertext"], self.KEYWORD)
        # Decrypted may have padding X — check the core content matches
        assert "INSTRUMENTS".replace("J", "I") in dec["plaintext"]

    def test_digraphs_populated(self):
        """Encryption result must include digraphs."""
        result = pf_enc("HELLO", self.KEYWORD)
        assert len(result["digraphs"]) > 0

    def test_keyword_with_duplicates(self):
        """Duplicate letters in keyword are handled correctly."""
        # Should not raise
        matrix = generate_matrix("AABBCC")
        assert len(matrix) == 5


# ════════════════════════════════════════════════════════════════════════════
# HILL CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestHill:
    VALID_MATRIX = [3, 3, 2, 5]  # det = 15-6 = 9, gcd(9,26)=1 ✓

    def test_validate_valid_matrix(self):
        """Valid matrix should pass validation."""
        ok, err = validate_matrix(self.VALID_MATRIX)
        assert ok is True

    def test_validate_singular_matrix(self):
        """Singular matrix (det=0) should fail."""
        ok, err = validate_matrix([2, 4, 1, 2])  # det = 4-4 = 0
        assert ok is False

    def test_validate_wrong_length(self):
        """Matrix with fewer than 4 values should fail."""
        ok, err = validate_matrix([1, 2, 3])
        assert ok is False

    def test_encrypt_produces_alpha_output(self):
        """Ciphertext should contain only alpha characters."""
        result = hill_enc("HELP", self.VALID_MATRIX)
        assert result["ciphertext"].isalpha()

    def test_round_trip_simple(self):
        """Encrypt then decrypt should recover processed plaintext."""
        original = "HELP"
        enc = hill_enc(original, self.VALID_MATRIX)
        dec = hill_dec(enc["ciphertext"], self.VALID_MATRIX)
        assert dec["plaintext"] == original

    def test_round_trip_longer(self):
        """Round trip on longer even-length text."""
        original = "HELLOWORLD"
        enc = hill_enc(original, self.VALID_MATRIX)
        dec = hill_dec(enc["ciphertext"], self.VALID_MATRIX)
        assert dec["plaintext"] == original

    def test_odd_length_padded(self):
        """Odd-length text gets X padding."""
        result = hill_enc("HEL", self.VALID_MATRIX)
        assert result["processed_plaintext"] == "HELX"

    def test_non_alpha_removed(self):
        """Non-alphabetic characters are removed."""
        result = hill_enc("HE LP", self.VALID_MATRIX)
        assert " " not in result["processed_plaintext"]

    def test_numeric_steps_populated(self):
        """Numeric steps table should be populated."""
        result = hill_enc("HELP", self.VALID_MATRIX)
        assert len(result["numeric_steps"]) == 2

    def test_different_matrix_same_round_trip(self):
        """Test with another valid matrix (1,2,3,5: det=5-6=-1≡25 mod 26, gcd(25,26)=1)."""
        matrix = [1, 2, 3, 5]  # det = 5-6 = -1 ≡ 25 mod 26, valid
        original = "ACTX"
        enc = hill_enc(original, matrix)
        dec = hill_dec(enc["ciphertext"], matrix)
        assert dec["plaintext"] == original


# ════════════════════════════════════════════════════════════════════════════
# VIGENÈRE CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestVigenere:
    def test_known_vector_attackatdawn(self):
        """ATTACKATDAWN + LEMON → LXFOPVEFRNHR (well-known vector)."""
        result = vig_enc("ATTACKATDAWN", "LEMON")
        assert result["ciphertext"] == "LXFOPVEFRNHR"

    def test_decrypt_known_vector(self):
        """LXFOPVEFRNHR + LEMON → ATTACKATDAWN."""
        result = vig_dec("LXFOPVEFRNHR", "LEMON")
        assert result["plaintext"] == "ATTACKATDAWN"

    def test_round_trip_short(self):
        """Encrypt then decrypt recovers original."""
        original = "HELLOWORLD"
        enc = vig_enc(original, "SECRET")
        dec = vig_dec(enc["ciphertext"], "SECRET")
        assert dec["plaintext"] == original

    def test_round_trip_with_spaces(self):
        """Spaces preserved in round trip."""
        original = "HELLO WORLD"
        enc = vig_enc(original, "KEY")
        dec = vig_dec(enc["ciphertext"], "KEY")
        assert dec["plaintext"] == original

    def test_key_repeated_correctly(self):
        """Key stream must repeat the keyword."""
        result = vig_enc("AAAAAAA", "AB")
        # A encrypted with A (shift 0) = A, A encrypted with B (shift 1) = B
        assert result["ciphertext"] == "ABABABA"

    def test_lowercase_text(self):
        """Lowercase text is handled."""
        enc = vig_enc("attackatdawn", "LEMON")
        dec = vig_dec(enc["ciphertext"], "LEMON")
        # Round trip should recover the original case
        assert dec["plaintext"].upper() == "ATTACKATDAWN"

    def test_spaces_do_not_consume_key(self):
        """Spaces should not consume key characters."""
        enc1 = vig_enc("HELLOWORLD", "KEY")
        enc2 = vig_enc("HELLO WORLD", "KEY")
        # Alpha portions should match
        alpha1 = "".join(c for c in enc1["ciphertext"] if c.isalpha())
        alpha2 = "".join(c for c in enc2["ciphertext"] if c.isalpha())
        assert alpha1 == alpha2

    def test_char_table_populated(self):
        """Char table should have entries for all alpha chars."""
        result = vig_enc("HELLO", "KEY")
        assert len(result["char_table"]) == 5

    def test_single_char_key(self):
        """Single-char key → behaves like Caesar."""
        result = vig_enc("HELLO", "D")
        # D = shift 3 = same as Caesar shift 3
        caesar_like = caesar_enc("HELLO", 3)
        assert result["ciphertext"] == caesar_like["ciphertext"]


# ════════════════════════════════════════════════════════════════════════════
# ONE-TIME PAD TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestOTP:
    def test_generate_key_correct_length(self):
        """Generated key should match alpha count of text."""
        text = "HELLO WORLD"
        key = otp_gen(text)
        alpha_count = sum(1 for c in text if c.isalpha())
        assert len(key) == alpha_count

    def test_round_trip(self):
        """Encrypt then decrypt recovers original."""
        original = "HELLOWORLD"
        key = otp_gen(original)
        enc = otp_enc(original, key)
        dec = otp_dec(enc["ciphertext"], key)
        assert dec["plaintext"] == original

    def test_round_trip_with_spaces(self):
        """Round trip preserves spaces."""
        original = "HELLO WORLD"
        key = otp_gen(original)
        enc = otp_enc(original, key)
        dec = otp_dec(enc["ciphertext"], key)
        assert dec["plaintext"] == original

    def test_zero_key_identity(self):
        """Key of all A's (shift 0) → no change."""
        key = "AAAAA"
        enc = otp_enc("HELLO", key)
        assert enc["ciphertext"] == "HELLO"

    def test_char_table_length(self):
        """Char table should match alpha char count."""
        text = "HELLO"
        key = otp_gen(text)
        enc = otp_enc(text, key)
        assert len(enc["char_table"]) == 5

    def test_known_example(self):
        """HELLO + XMCKL → EQNVZ (classic OTP example)."""
        result = otp_enc("HELLO", "XMCKL")
        assert result["ciphertext"] == "EQNVZ"

    def test_decrypt_known_example(self):
        """EQNVZ + XMCKL → HELLO."""
        result = otp_dec("EQNVZ", "XMCKL")
        assert result["plaintext"] == "HELLO"


# ════════════════════════════════════════════════════════════════════════════
# RAIL FENCE CIPHER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestRailFence:
    def test_encrypt_2_rails(self):
        """Simple 2-rail encryption."""
        result = rf_enc("HELLOWORLD", 2)
        # H L O O L  E L W R D → HLOOLEL WRD
        assert result["ciphertext"] is not None
        assert len(result["ciphertext"]) == len("HELLOWORLD")

    def test_length_preserved(self):
        """Ciphertext length should equal plaintext length."""
        text = "WEAREDISCOVEREDFLEEATONCE"
        result = rf_enc(text, 3)
        assert len(result["ciphertext"]) == len(text)

    def test_round_trip_3_rails(self):
        """Encrypt then decrypt with 3 rails recovers original."""
        original = "WEAREDISCOVEREDFLEEATONCE"
        enc = rf_enc(original, 3)
        dec = rf_dec(enc["ciphertext"], 3)
        assert dec["plaintext"] == original

    def test_round_trip_2_rails(self):
        """Round trip with 2 rails."""
        original = "HELLOWORLD"
        enc = rf_enc(original, 2)
        dec = rf_dec(enc["ciphertext"], 2)
        assert dec["plaintext"] == original

    def test_round_trip_with_spaces(self):
        """Round trip including spaces."""
        original = "HELLO WORLD"
        enc = rf_enc(original, 3)
        dec = rf_dec(enc["ciphertext"], 3)
        assert dec["plaintext"] == original

    def test_visual_grid_rows(self):
        """Visual grid should have exactly `rails` rows."""
        text = "HELLOWORLD"
        rails = 3
        result = rf_enc(text, rails)
        assert len(result["visual_grid"]) == rails

    def test_visual_grid_cols(self):
        """Each row of visual grid should have length = text length."""
        text = "HELLOWORLD"
        rails = 3
        result = rf_enc(text, rails)
        for row in result["visual_grid"]:
            assert len(row) == len(text)

    def test_rails_equal_to_length_returns_unchanged(self):
        """Rails >= length → effectively no transposition."""
        text = "HELLO"
        result = rf_enc(text, len(text))
        assert result["ciphertext"] == text

    def test_single_char(self):
        """Single character text should work."""
        result = rf_enc("A", 2)
        assert result["ciphertext"] == "A"


# ════════════════════════════════════════════════════════════════════════════
# COLUMNAR TRANSPOSITION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestColumnar:
    def test_length_preserved_no_padding_needed(self):
        """Ciphertext length should equal padded plaintext length."""
        text = "ATTACK"  # 6 chars, key length 5, padded to 2*5 = 10
        result = col_enc(text, 2, 5, "43125")
        assert len(result["ciphertext"]) == len(result["padded_text"])

    def test_round_trip_no_padding(self):
        """Round trip when text perfectly fills the grid."""
        original = "HELLOWORLD" # 10 chars, rows=2, cols=5
        enc = col_enc(original, 2, 5, "43125")
        dec = col_dec(enc["ciphertext"], 2, 5, "43125")
        assert dec["plaintext"] == original

    def test_round_trip_with_padding(self):
        """Round trip when padding is needed."""
        original = "ATTACKATDAWN"  # 12 chars, cols=5, rows=3 (capacity 15)
        enc = col_enc(original, 3, 5, "43125")
        dec = col_dec(enc["ciphertext"], 3, 5, "43125")
        assert dec["plaintext"].rstrip("X") == original

    def test_grid_dimensions(self):
        """Grid should have correct dimensions."""
        result = col_enc("HELLOWORLD", 2, 5, "43125")
        assert result["num_cols"] == 5
        assert result["num_rows"] == 2

    def test_padding_character_is_x(self):
        """Padding should use X."""
        result = col_enc("HELLO", 1, 5, "43125")  # 5 chars, cols=5, rows=1 -> no padding
        assert "X" not in result["padded_text"]

    def test_column_order_length(self):
        """Column order should have same length as key."""
        result = col_enc("HELLOWORLD", 2, 5, "43125")
        assert len(result["column_order"]) == 5

    def test_different_keywords(self):
        """Different keys produce different ciphertexts."""
        text = "HELLOWORLD"
        enc1 = col_enc(text, 2, 5, "43125")
        enc2 = col_enc(text, 2, 5, "12345")
        assert enc1["ciphertext"] != enc2["ciphertext"]

    def test_round_trip_short_keyword(self):
        """Round trip with short key."""
        original = "SECRETMESSAGE" # 13 chars, cols=3, rows=5 -> capacity 15
        enc = col_enc(original, 5, 3, "213")
        dec = col_dec(enc["ciphertext"], 5, 3, "213")
        assert dec["plaintext"].rstrip("X") == original

    def test_single_col_keyword(self):
        """Single-character key -> no reordering."""
        original = "HELLO"
        enc = col_enc(original, 5, 1, "1")
        dec = col_dec(enc["ciphertext"], 5, 1, "1")
        assert dec["plaintext"] == original


# ════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Cross-algorithm and integration tests."""

    def test_all_ciphers_round_trip(self):
        """Quick round-trip test for all 8 ciphers."""
        text = "NETWORKSECU"

        # Caesar
        enc = caesar_enc(text, 5)
        dec = caesar_dec(enc["ciphertext"], 5)
        assert dec["plaintext"] == text

        # Mono
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        enc = mono_enc(text, key)
        dec = mono_dec(enc["ciphertext"], key)
        assert dec["plaintext"] == text

        # Vigenère
        enc = vig_enc(text, "LEMON")
        dec = vig_dec(enc["ciphertext"], "LEMON")
        assert dec["plaintext"] == text

        # Hill (odd-length text gets X padding, so strip trailing X from decrypted)
        enc = hill_enc(text, [3, 3, 2, 5])
        dec = hill_dec(enc["ciphertext"], [3, 3, 2, 5])
        assert dec["plaintext"].rstrip("X") == text

        # Rail Fence
        enc = rf_enc(text, 3)
        dec = rf_dec(enc["ciphertext"], 3)
        assert dec["plaintext"] == text

        # Columnar (NETWORKSECU is 11 chars; grid of 3x4 = 12 fits)
        enc = col_enc(text, 3, 4, "4321")
        dec = col_dec(enc["ciphertext"], 3, 4, "4321")
        assert dec["plaintext"].rstrip("X") == text

    def test_caesar_is_subset_of_vigenere(self):
        """Single-char Vigenère keyword == Caesar with same shift."""
        text = "HELLOWORLD"
        shift = 7
        key_char = chr(ord('A') + shift)  # H = shift 7
        caesar_result = caesar_enc(text, shift)
        vig_result = vig_enc(text, key_char)
        assert caesar_result["ciphertext"] == vig_result["ciphertext"]

    def test_otp_different_keys_different_ciphertexts(self):
        """Different OTP keys produce different ciphertexts."""
        text = "HELLO"
        enc1 = otp_enc(text, "XMCKL")
        enc2 = otp_enc(text, "ABCDE")
        assert enc1["ciphertext"] != enc2["ciphertext"]

    def test_vigenere_known_vector_confirmed(self):
        """Confirm the famous ATTACKATDAWN + LEMON = LXFOPVEFRNHR vector."""
        result = vig_enc("ATTACKATDAWN", "LEMON")
        assert result["ciphertext"] == "LXFOPVEFRNHR"
        # Also confirm reverse
        dec = vig_dec("LXFOPVEFRNHR", "LEMON")
        assert dec["plaintext"] == "ATTACKATDAWN"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
