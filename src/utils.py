"""
BhashaAI — Utility Functions
Timer, text statistics, and helper functions.
"""

import time
from contextlib import contextmanager


@contextmanager
def timer():
    """Context manager that measures elapsed time in seconds.

    Usage:
        with timer() as t:
            do_work()
        print(f"Took {t.elapsed:.3f}s")
    """
    class TimerResult:
        elapsed = 0.0

    result = TimerResult()
    start = time.perf_counter()
    try:
        yield result
    finally:
        result.elapsed = time.perf_counter() - start


def word_count(text: str) -> int:
    """Count words in text."""
    if not text or not text.strip():
        return 0
    return len(text.split())


def char_count(text: str) -> int:
    """Count characters in text (excluding leading/trailing whitespace)."""
    if not text:
        return 0
    return len(text.strip())


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable string."""
    if seconds < 1.0:
        return f"{seconds * 1000:.0f} ms"
    elif seconds < 60.0:
        return f"{seconds:.2f} s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_number(n: int) -> str:
    """Format a number with commas (e.g. 1,248)."""
    return f"{n:,}"
