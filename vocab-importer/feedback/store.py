import os
import json
import sqlite3
from datetime import datetime
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
    
    # Create feedback table if it doesn't exist
    create_feedback_table(conn)
    
    return conn

def create_feedback_table(conn):
    """
    Create feedback table if it doesn't exist
    
    Args:
        conn (sqlite3.Connection): Database connection
    """
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY,
        session_id TEXT NOT NULL,
        theme TEXT NOT NULL,
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT,
        timestamp TEXT NOT NULL
    )
    ''')
    
    conn.commit()

def store_feedback(session_id, theme, provider, model, rating, comments=None):
    """
    Store feedback in the database
    
    Args:
        session_id (str): Session ID
        theme (str): Theme/category
        provider (str): LLM provider
        model (str): Model name
        rating (int): Rating (1-5)
        comments (str, optional): Comments
        
    Returns:
        int: Feedback ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute(
        """
        INSERT INTO feedback (session_id, theme, provider, model, rating, comments, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (session_id, theme, provider, model, rating, comments, timestamp)
    )
    
    feedback_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return feedback_id

def get_feedback(session_id=None, limit=10):
    """
    Get feedback from the database
    
    Args:
        session_id (str, optional): Session ID to filter by
        limit (int, optional): Maximum number of feedback items to return
        
    Returns:
        list: List of feedback dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if session_id:
        cursor.execute(
            "SELECT * FROM feedback WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (session_id, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM feedback ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
    
    results = cursor.fetchall()
    
    # Convert to dictionaries
    feedback_list = []
    for row in results:
        feedback_list.append(dict(row))
    
    conn.close()
    
    return feedback_list

def get_feedback_stats():
    """
    Get feedback statistics
    
    Returns:
        dict: Feedback statistics
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get average rating
    cursor.execute("SELECT AVG(rating) as avg_rating FROM feedback")
    avg_rating = cursor.fetchone()['avg_rating'] or 0
    
    # Get rating distribution
    cursor.execute(
        """
        SELECT rating, COUNT(*) as count
        FROM feedback
        GROUP BY rating
        ORDER BY rating
        """
    )
    rating_distribution = {}
    for row in cursor.fetchall():
        rating_distribution[row['rating']] = row['count']
    
    # Get provider statistics
    cursor.execute(
        """
        SELECT provider, AVG(rating) as avg_rating, COUNT(*) as count
        FROM feedback
        GROUP BY provider
        ORDER BY avg_rating DESC
        """
    )
    provider_stats = {}
    for row in cursor.fetchall():
        provider_stats[row['provider']] = {
            'avg_rating': row['avg_rating'],
            'count': row['count']
        }
    
    # Get model statistics
    cursor.execute(
        """
        SELECT model, AVG(rating) as avg_rating, COUNT(*) as count
        FROM feedback
        GROUP BY model
        ORDER BY avg_rating DESC
        """
    )
    model_stats = {}
    for row in cursor.fetchall():
        model_stats[row['model']] = {
            'avg_rating': row['avg_rating'],
            'count': row['count']
        }
    
    # Get theme statistics
    cursor.execute(
        """
        SELECT theme, AVG(rating) as avg_rating, COUNT(*) as count
        FROM feedback
        GROUP BY theme
        ORDER BY count DESC
        LIMIT 10
        """
    )
    theme_stats = {}
    for row in cursor.fetchall():
        theme_stats[row['theme']] = {
            'avg_rating': row['avg_rating'],
            'count': row['count']
        }
    
    conn.close()
    
    return {
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
        'provider_stats': provider_stats,
        'model_stats': model_stats,
        'theme_stats': theme_stats
    }

def export_feedback(filename=None):
    """
    Export feedback to a JSON file
    
    Args:
        filename (str, optional): Output filename. If None, a default name is generated.
        
    Returns:
        str: Path to the exported file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
    results = cursor.fetchall()
    
    # Convert to dictionaries
    feedback_list = []
    for row in results:
        feedback_list.append(dict(row))
    
    conn.close()
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"feedback_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(feedback_list, f, indent=2)
    
    return filepath 