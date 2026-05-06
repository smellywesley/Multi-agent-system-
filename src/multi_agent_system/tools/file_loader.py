"""Utility for loading text files."""

from pathlib import Path


def load_text(path: str | Path) -> str:
    """Load UTF-8 text from file path."""
    return Path(path).read_text(encoding="utf-8")
