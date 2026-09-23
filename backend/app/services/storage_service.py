"""
Storage Service
SQLite persistence for translation history, phrasebook favorites, and saved dialogues.
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assistant_storage.db")

class StorageService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # History table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS translation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                domain TEXT DEFAULT 'general',
                tone TEXT DEFAULT 'neutral',
                fidelity_score REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Phrasebook table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS phrasebook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Pre-seed phrasebook with essential multilingual phrases if empty
            cursor.execute("SELECT COUNT(*) FROM phrasebook")
            if cursor.fetchone()[0] == 0:
                sample_phrases = [
                    ("मुझे कल कॉलेज जाना है।", "hi", "I have to go to college tomorrow.", "en", "Academic", "Aryan's Slide 9 Example"),
                    ("I am going to college.", "en", "मैं कॉलेज जा रहा हूँ।", "hi", "Everyday", "Aryan's Slide 6 Transformer Example"),
                    ("Hello, how are you?", "en", "नमस्ते, आप कैसे हैं?", "hi", "Greetings", "Polite formal greeting with 'आप'"),
                    ("Where is the nearest hospital?", "en", "निकटतम अस्पताल कहाँ है?", "hi", "Travel / Healthcare", "Essential emergency phrase"),
                    ("Natural Language Processing enables cross-lingual intelligence.", "en", "प्राकृतिक भाषा प्रसंस्करण क्रॉस-भाषी बुद्धिमत्ता को सक्षम बनाता है।", "hi", "Tech", "Multilingual NLP Core Definition")
                ]
                cursor.executemany("""
                INSERT INTO phrasebook (source_text, source_lang, translated_text, target_lang, category, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """, sample_phrases)

            conn.commit()

    def add_history(self, source_text: str, source_lang: str, translated_text: str, target_lang: str, domain: str = "general", tone: str = "neutral", fidelity_score: float = 1.0) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO translation_history (source_text, source_lang, translated_text, target_lang, domain, tone, fidelity_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (source_text, source_lang, translated_text, target_lang, domain, tone, fidelity_score))
            conn.commit()
            return cursor.lastrowid

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, source_text, source_lang, translated_text, target_lang, domain, tone, fidelity_score, created_at
            FROM translation_history
            ORDER BY id DESC
            LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def clear_history(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM translation_history")
            conn.commit()

    def add_phrase(self, source_text: str, source_lang: str, translated_text: str, target_lang: str, category: str = "General", notes: str = "") -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO phrasebook (source_text, source_lang, translated_text, target_lang, category, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (source_text, source_lang, translated_text, target_lang, category, notes))
            conn.commit()
            return cursor.lastrowid

    def get_phrasebook(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if category and category.lower() != "all":
                cursor.execute("""
                SELECT id, source_text, source_lang, translated_text, target_lang, category, notes, created_at
                FROM phrasebook
                WHERE category = ?
                ORDER BY id DESC
                """, (category,))
            else:
                cursor.execute("""
                SELECT id, source_text, source_lang, translated_text, target_lang, category, notes, created_at
                FROM phrasebook
                ORDER BY id DESC
                """)
            return [dict(row) for row in cursor.fetchall()]

    def delete_phrase(self, phrase_id: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM phrasebook WHERE id = ?", (phrase_id,))
            conn.commit()

storage_service = StorageService()
