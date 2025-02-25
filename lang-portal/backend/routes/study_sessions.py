from fastapi import APIRouter, HTTPException, Query, Path, Body
from lib.db import get_db_connection
from models import PaginatedStudySessions, StudySession, PaginatedWords, WordReview
from utils import paginate
from datetime import datetime
import json

router = APIRouter()

@router.get("/study_sessions", response_model=PaginatedStudySessions, tags=["Study Sessions"])
def get_study_sessions(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of study sessions.

    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        query = """
        SELECT ss.id,
               sa.name AS activity_name,
               g.name AS group_name,
               ss.created_at AS start_time,
               NULL AS end_time,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = ss.id) as review_items_count
        FROM study_sessions ss
        LEFT JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN groups g ON g.id = ss.group_id
        ORDER BY ss.created_at DESC
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query)
        rows = cursor.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail="No study sessions found")
        
        # Convert rows to list of StudySession models
        study_sessions = [
            {
                "id": row[0],
                "activity_name": row[1],
                "group_name": row[2],
                "start_time": row[3],
                "end_time": row[4],
                "review_items_count": row[5]
            } for row in rows
        ]

        # Calculate total items and total pages
        total_items = conn.execute("SELECT COUNT(*) FROM study_sessions").fetchone()[0]
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            "study_sessions": study_sessions,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "items_per_page": page_size
            }
        }

@router.get("/study_sessions/{session_id}", response_model=StudySession, tags=["Study Sessions"])
def get_study_session(session_id: int = Path(..., title="The ID of the study session to retrieve")):
    """
    Retrieve a specific study session by ID.

    - **session_id**: The ID of the study session to retrieve.
    """
    with get_db_connection() as conn:
        query = """
        SELECT ss.id,
               sa.name AS activity_name,
               g.name AS group_name,
               ss.created_at AS start_time,
               NULL AS end_time,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = ss.id) as review_items_count
        FROM study_sessions ss
        LEFT JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN groups g ON g.id = ss.group_id
        WHERE ss.id = ?
        """
        cursor = conn.execute(query, (session_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Study session not found")
        
        # Convert row to StudySession model
        study_session = StudySession(
            id=row[0],
            activity_name=row[1],
            group_name=row[2],
            start_time=row[3],
            end_time=row[4],
            review_items_count=row[5]
        ).model_dump()
        
        return study_session 

@router.get("/study_sessions/{session_id}/words", response_model=PaginatedWords, tags=["Study Sessions"])
def get_session_words(
    session_id: int = Path(..., title="The ID of the study session to retrieve words for"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Retrieve a paginated list of words for a specific study session.

    - **session_id**: The ID of the study session to retrieve words for.
    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # First check if the session exists
        session_exists = conn.execute(
            "SELECT 1 FROM study_sessions WHERE id = ?", 
            (session_id,)
        ).fetchone()
        
        if not session_exists:
            raise HTTPException(status_code=404, detail="Study session not found")

        # Query to get words for the session
        query = """
        SELECT w.id, w.jamaican_patois, w.english, w.parts,
               COALESCE(SUM(CASE WHEN wr.correct THEN 1 ELSE 0 END), 0) as correct_count,
               COALESCE(SUM(CASE WHEN NOT wr.correct THEN 1 ELSE 0 END), 0) as wrong_count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        LEFT JOIN word_reviews wr ON wr.word_id = w.id
        WHERE wri.study_session_id = ?
        GROUP BY w.id
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query, (session_id,))
        rows = cursor.fetchall()
        
        if not rows:
            raise HTTPException(
                status_code=404, 
                detail="No words found for this study session"
            )
        
        # Convert rows to list of Word models
        words = [
            {
                "id": row[0],
                "jamaican_patois": row[1],
                "english": row[2],
                "parts": json.loads(row[3]) if row[3] else None,
                "correct_count": row[4],
                "wrong_count": row[5]
            } for row in rows
        ]

        # Get total count for pagination
        total_items = conn.execute(
            """
            SELECT COUNT(DISTINCT w.id)
            FROM words w
            JOIN word_review_items wri ON wri.word_id = w.id
            WHERE wri.study_session_id = ?
            """, 
            (session_id,)
        ).fetchone()[0]
        
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            "words": words,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "items_per_page": page_size
            }
        } 

@router.post("/study_sessions/{session_id}/words/{word_id}/review", response_model=WordReview, tags=["Study Sessions"])
def create_word_review(
    session_id: int = Path(..., title="The ID of the study session"),
    word_id: int = Path(..., title="The ID of the word being reviewed"),
    correct: bool = Body(..., embed=True)
):
    """
    Record a word review during a study session.

    - **session_id**: The ID of the study session
    - **word_id**: The ID of the word being reviewed
    - **correct**: Whether the word was reviewed correctly
    """
    with get_db_connection() as conn:
        # Check if session exists
        session_exists = conn.execute(
            "SELECT 1 FROM study_sessions WHERE id = ?",
            (session_id,)
        ).fetchone()
        
        if not session_exists:
            raise HTTPException(status_code=404, detail="Study session not found")

        # Check if word exists
        word = conn.execute(
            """
            SELECT jamaican_patois, english 
            FROM words 
            WHERE id = ?
            """,
            (word_id,)
        ).fetchone()
        
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        # Create word review item if it doesn't exist
        conn.execute(
            """
            INSERT OR IGNORE INTO word_review_items (study_session_id, word_id)
            VALUES (?, ?)
            """,
            (session_id, word_id)
        )

        # Create the word review
        current_time = datetime.now().isoformat()
        cursor = conn.execute(
            """
            INSERT INTO word_reviews (word_id, study_session_id, correct, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (word_id, session_id, correct, current_time)
        )
        review_id = cursor.lastrowid

        return {
            "id": review_id,
            "word_id": word_id,
            "study_session_id": session_id,
            "correct": correct,
            "created_at": current_time,
            "word_jamaican_patois": word[0],
            "word_english": word[1]
        } 