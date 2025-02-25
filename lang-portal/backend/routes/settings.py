from fastapi import APIRouter, HTTPException
from lib.db import get_db_connection
from pydantic import BaseModel

router = APIRouter()

class LearningPreferences(BaseModel):
    wordsPerSession: int
    reviewInterval: int
    showPhonetics: bool
    showUsageExamples: bool
    darkMode: bool

@router.get("/settings", response_model=LearningPreferences, tags=["Settings"])
def get_settings():
    """
    Retrieve user's learning preferences.
    """
    with get_db_connection() as conn:
        # Set row_factory to get dictionary-like results
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        
        # Check if settings exist
        settings = conn.execute(
            "SELECT * FROM user_settings WHERE id = 1"
        ).fetchone()

        if not settings:
            # Return default settings
            return {
                "wordsPerSession": 10,
                "reviewInterval": 24,
                "showPhonetics": True,
                "showUsageExamples": True,
                "darkMode": True
            }

        return {
            "wordsPerSession": settings["words_per_session"],
            "reviewInterval": settings["review_interval"],
            "showPhonetics": bool(settings["show_phonetics"]),
            "showUsageExamples": bool(settings["show_usage_examples"]),
            "darkMode": bool(settings["dark_mode"])
        }

@router.post("/settings", response_model=LearningPreferences, tags=["Settings"])
def update_settings(preferences: LearningPreferences):
    """
    Update user's learning preferences.
    """
    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO user_settings (
                id, words_per_session, review_interval, 
                show_phonetics, show_usage_examples, dark_mode
            ) VALUES (
                1, ?, ?, ?, ?, ?
            )
        """, (
            preferences.wordsPerSession,
            preferences.reviewInterval,
            preferences.showPhonetics,
            preferences.showUsageExamples,
            preferences.darkMode
        ))

        return preferences 