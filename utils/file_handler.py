"""
File Handler Utility
====================
Helpers for reading uploaded files and creating downloadable content.
"""

import io
from typing import Optional


def read_uploaded_file(uploaded_file) -> tuple[bool, str, str]:
    """
    Read content from a Streamlit UploadedFile object.

    Args:
        uploaded_file: st.file_uploader result object.

    Returns:
        (success, content, error_message)
    """
    if uploaded_file is None:
        return False, "", "No file uploaded."

    try:
        # Read bytes and decode as UTF-8
        raw = uploaded_file.read()
        content = raw.decode("utf-8")
        if not content.strip():
            return False, "", "The uploaded file is empty."
        return True, content, ""
    except UnicodeDecodeError:
        return False, "", "Could not read file. Please upload a plain text (.txt) file encoded in UTF-8."
    except Exception as e:
        return False, "", f"Error reading file: {str(e)}"


def create_download_content(text: str, filename: str = "result.txt") -> tuple[bytes, str]:
    """
    Prepare text content for Streamlit download button.

    Args:
        text: The text content to download.
        filename: Suggested filename.

    Returns:
        (bytes_content, mime_type)
    """
    return text.encode("utf-8"), "text/plain"


def get_file_stats(content: str) -> dict:
    """
    Return basic statistics about file content.

    Args:
        content: Text content.

    Returns:
        dict with character_count, word_count, line_count, alpha_count.
    """
    return {
        "character_count": len(content),
        "word_count": len(content.split()),
        "line_count": content.count("\n") + 1,
        "alpha_count": sum(1 for ch in content if ch.isalpha()),
    }
