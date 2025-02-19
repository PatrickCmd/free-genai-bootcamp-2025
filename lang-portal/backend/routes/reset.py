from fastapi import APIRouter, HTTPException
from lib.db import get_db_connection
import os

router = APIRouter()

# Only enable these endpoints in development/testing
ENABLE_RESET = os.getenv("ENABLE_RESET", "false").lower() == "true"

@router.post("/reset/all", tags=["Reset"])
async def reset_all_data():
    """
    Reset all data in the database. Only available in development/testing.
    """
    if not ENABLE_RESET:
        raise HTTPException(
            status_code=403,
            detail="Reset endpoints are disabled in production"
        )
    
    with get_db_connection() as conn:
        # Delete data in reverse order of dependencies
        conn.execute("DELETE FROM word_reviews")
        conn.execute("DELETE FROM word_review_items")
        conn.execute("DELETE FROM study_sessions")
        conn.execute("DELETE FROM study_activities")
        conn.execute("DELETE FROM words")
        conn.execute("DELETE FROM groups")
        
        # Reset auto-increment counters
        conn.execute("DELETE FROM sqlite_sequence")
        
        return {"message": "All data has been reset"}

@router.post("/reset/study-data", tags=["Reset"])
async def reset_study_data():
    """
    Reset only study-related data, preserving words and groups.
    """
    if not ENABLE_RESET:
        raise HTTPException(
            status_code=403,
            detail="Reset endpoints are disabled in production"
        )
    
    with get_db_connection() as conn:
        # Delete study-related data
        conn.execute("DELETE FROM word_reviews")
        conn.execute("DELETE FROM word_review_items")
        conn.execute("DELETE FROM study_sessions")
        conn.execute("DELETE FROM study_activities")
        
        # Reset auto-increment counters for affected tables
        conn.execute("""
            DELETE FROM sqlite_sequence 
            WHERE name IN (
                'word_reviews', 
                'word_review_items', 
                'study_sessions', 
                'study_activities'
            )
        """)
        
        return {"message": "Study data has been reset"}

@router.post("/reset/seed", tags=["Reset"])
async def seed_test_data():
    """
    Seed the database with test data. Only available in development/testing.
    """
    if not ENABLE_RESET:
        raise HTTPException(
            status_code=403,
            detail="Reset endpoints are disabled in production"
        )
    
    with get_db_connection() as conn:
        # Create test groups
        conn.execute("""
            INSERT INTO groups (name, description) VALUES 
            ('Beginner Patois', 'Basic vocabulary and phrases'),
            ('Intermediate Patois', 'More complex expressions'),
            ('Advanced Patois', 'Advanced language concepts')
        """)
        
        # Create test words
        conn.execute("""
            INSERT INTO words (jamaican_patois, english, parts, group_id) VALUES 
            ('mi', 'me/my', '{"type":"pronoun","usage":"subject"}', 1),
            ('yuh', 'you', '{"type":"pronoun","usage":"subject"}', 1),
            ('dem', 'them/they', '{"type":"pronoun","usage":"subject"}', 1),
            ('nyam', 'eat', '{"type":"verb","usage":"action"}', 2),
            ('gwaan', 'go on/continue', '{"type":"verb","usage":"action"}', 2)
        """)
        
        # Create test study activities
        conn.execute("""
            INSERT INTO study_activities (name, group_id, created_at) VALUES 
            ('Vocabulary Review', 1, datetime('now')),
            ('Grammar Practice', 2, datetime('now'))
        """)
        
        # Create test study sessions
        conn.execute("""
            INSERT INTO study_sessions (study_activity_id, group_id, created_at) VALUES 
            (1, 1, datetime('now')),
            (2, 2, datetime('now'))
        """)
        
        # Add words to review items
        conn.execute("""
            INSERT INTO word_review_items (study_session_id, word_id) 
            SELECT 1, id FROM words WHERE group_id = 1
            UNION
            SELECT 2, id FROM words WHERE group_id = 2
        """)
        
        # Add some word reviews
        conn.execute("""
            INSERT INTO word_reviews (word_id, study_session_id, correct, created_at)
            SELECT 
                word_id, 
                study_session_id, 
                CASE WHEN RANDOM() > 0.3 THEN TRUE ELSE FALSE END,
                datetime('now', '-' || RANDOM() * 10 || ' minutes')
            FROM word_review_items
        """)
        
        return {"message": "Test data has been seeded"} 