"""
BhashaAI — Translation History
JSON-based storage for recent translations, with SQLite upgrade path.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import HISTORY_FILE

logger = logging.getLogger(__name__)


def _ensure_file():
    """Ensure the history JSON file exists."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")


def load_history() -> List[Dict[str, Any]]:
    """Load all translation history records."""
    _ensure_file()
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Failed to load history: {e}")
        return []


def save_translation(
    source_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
    translation_time: float = 0.0,
    detected_lang: Optional[str] = None,
) -> Dict[str, Any]:
    """Save a translation to history and return the record."""
    record = {
        "source_text": source_text,
        "translated_text": translated_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "translation_time": round(translation_time, 3),
        "detected_lang": detected_lang,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "timestamp_iso": datetime.now().isoformat(),
    }

    history = load_history()
    history.insert(0, record)  # newest first

    # Keep max 100 records
    history = history[:100]

    try:
        HISTORY_FILE.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        logger.error(f"Failed to save history: {e}")

    return record


def clear_history():
    """Delete all history records."""
    _ensure_file()
    try:
        HISTORY_FILE.write_text("[]", encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to clear history: {e}")


def get_recent(n: int = 20) -> List[Dict[str, Any]]:
    """Get the N most recent translations."""
    history = load_history()
    return history[:n]
