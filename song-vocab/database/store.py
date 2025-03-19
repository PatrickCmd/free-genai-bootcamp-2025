import sqlite3
import json
from typing import List, Optional
from .models import Song, Vocabulary, SongBase, VocabularyBase

class DatabaseStore:
    def __init__(self, db_path: str = "data/vocab.db"):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        return sqlite3.connect(self.db_path)

    def add_song(self, song: SongBase) -> int:
        """Add a new song to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO songs (title, lyrics, language, artist, album, release_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (song.title, song.lyrics, song.language, song.artist, song.album, song.release_date)
        )
        
        song_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return song_id

    def add_vocabulary(self, vocab: VocabularyBase) -> int:
        """Add new vocabulary to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO vocabulary (song_id, word, explanation, example_sentences)
            VALUES (?, ?, ?, ?)
            """,
            (
                vocab.song_id,
                vocab.word,
                vocab.explanation,
                json.dumps(vocab.example_sentences)
            )
        )
        
        vocab_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return vocab_id

    def get_song(self, song_id: int) -> Optional[Song]:
        """Get a song by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Song(
                id=row[0],
                title=row[1],
                lyrics=row[2],
                language=row[3],
                artist=row[4],
                album=row[5],
                release_date=row[6]
            )
        return None

    def get_vocabulary_for_song(self, song_id: int):
        """Get vocabulary for a specific song and convert example_sentences back to lists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, song_id, word, explanation, example_sentences
            FROM vocabulary
            WHERE song_id = ?
        """, (song_id,))
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            vocab_dict = {
                "id": row[0],
                "song_id": row[1],
                "word": row[2],
                "explanation": row[3],
                "example_sentences": row[4].split("|||") if row[4] else []
            }
            result.append(vocab_dict)
        
        conn.close()
        return result 