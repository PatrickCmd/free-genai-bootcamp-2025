import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database path from environment or use default
DB_PATH = os.getenv("DATABASE_PATH", "data/db/vocabulary.db")

def get_connection():
    """
    Get a connection to the SQLite database
    
    Returns:
        sqlite3.Connection: Database connection
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    
    # Create tables if they don't exist
    create_tables(conn)
    
    return conn

def create_tables(conn):
    """
    Create database tables if they don't exist
    
    Args:
        conn (sqlite3.Connection): Database connection
    """
    cursor = conn.cursor()
    
    # Create words table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        jamaican_patois TEXT NOT NULL,
        english TEXT NOT NULL,
        type TEXT NOT NULL,
        usage TEXT
    )
    ''')
    
    # Create groups table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Create word_groups table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS word_groups (
        id INTEGER PRIMARY KEY,
        word_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        FOREIGN KEY (word_id) REFERENCES words (id),
        FOREIGN KEY (group_id) REFERENCES groups (id),
        UNIQUE (word_id, group_id)
    )
    ''')
    
    conn.commit()

def get_group_id(name):
    """
    Get the ID of a group by name, or None if it doesn't exist
    
    Args:
        name (str): Group name
        
    Returns:
        int or None: Group ID if found, None otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM groups WHERE name = ?", (name,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result['id'] if result else None

def get_last_group_id():
    """
    Get the last (highest) group ID in the database
    
    Returns:
        int: Last group ID, or 0 if no groups exist
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id) as max_id FROM groups")
    result = cursor.fetchone()
    
    conn.close()
    
    return result['max_id'] or 0

def get_last_word_id():
    """
    Get the last (highest) word ID in the database
    
    Returns:
        int: Last word ID, or 0 if no words exist
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id) as max_id FROM words")
    result = cursor.fetchone()
    
    conn.close()
    
    return result['max_id'] or 0

def get_last_word_group_id():
    """
    Get the last (highest) word_group ID in the database
    
    Returns:
        int: Last word_group ID, or 0 if no word_groups exist
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id) as max_id FROM word_groups")
    result = cursor.fetchone()
    
    conn.close()
    
    return result['max_id'] or 0

def check_database_exists():
    """
    Check if the database file exists
    
    Returns:
        bool: True if the database exists, False otherwise
    """
    return os.path.exists(DB_PATH) 