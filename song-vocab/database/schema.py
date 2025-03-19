import sqlite3
from pathlib import Path

# SQL statements for creating tables
CREATE_SONGS_TABLE = """
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    lyrics TEXT NOT NULL,
    language TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT,
    release_date DATE
)
"""

CREATE_VOCABULARY_TABLE = """
CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER NOT NULL,
    word TEXT NOT NULL,
    explanation TEXT NOT NULL,
    example_sentences TEXT NOT NULL,
    FOREIGN KEY (song_id) REFERENCES songs (id)
)
"""

def init_db(db_path: str = "data/vocab.db"):
    """Initialize the database and create tables if they don't exist"""
    # Ensure the data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database and create tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute(CREATE_SONGS_TABLE)
    cursor.execute(CREATE_VOCABULARY_TABLE)
    
    # Commit changes and close connection
    conn.commit()
    conn.close() 