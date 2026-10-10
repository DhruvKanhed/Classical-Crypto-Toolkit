"""
Timing Utility
==============
Helper for measuring execution time of cipher operations.
"""

import time
from typing import Callable, Any


def measure_time(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Measure the execution time of a function call.

    Args:
        func: The function to call.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        (result, elapsed_seconds) tuple.
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def format_time(seconds: float) -> str:
    """Format elapsed time as a human-readable string."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f} µs"
    elif seconds < 1.0:
        return f"{seconds * 1_000:.4f} ms"
    else:
        return f"{seconds:.4f} s"
