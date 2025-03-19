from datetime import date
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from database import SongBase, VocabularyBase, init_db, DatabaseStore

def test_database_operations():
    """Test basic database operations"""
    # Use a test database file
    test_db_path = "data/test_vocab.db"
    
    # Initialize the database
    init_db(test_db_path)
    db = DatabaseStore(test_db_path)
    
    # Test adding a song
    test_song = SongBase(
        title="Despacito",
        lyrics="Despacito\nQuiero respirar tu cuello despacito...",
        language="Spanish",
        artist="Luis Fonsi",
        album="Vida",
        release_date=date(2017, 1, 13)
    )
    
    song_id = db.add_song(test_song)
    print(f"Added song with ID: {song_id}")
    
    # Test retrieving the song
    retrieved_song = db.get_song(song_id)
    print(f"Retrieved song: {retrieved_song.title} by {retrieved_song.artist}")
    
    # Test adding vocabulary
    test_vocab = VocabularyBase(
        song_id=song_id,
        word="despacito",
        explanation="Slowly (adverb); diminutive of 'despacio' (slow)",
        example_sentences=[
            "Vamos a bailar despacito.",
            "Habla despacito, por favor."
        ]
    )
    
    vocab_id = db.add_vocabulary(test_vocab)
    print(f"Added vocabulary with ID: {vocab_id}")
    
    # Test retrieving vocabulary
    vocab_entries = db.get_vocabulary_for_song(song_id)
    print(f"Retrieved {len(vocab_entries)} vocabulary entries")
    for vocab in vocab_entries:
        print(f"Word: {vocab.word}")
        print(f"Explanation: {vocab.explanation}")
        print(f"Example sentences: {vocab.example_sentences}")

if __name__ == "__main__":
    test_database_operations() 