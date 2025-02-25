from fastapi import APIRouter, HTTPException, Path, Query, Body
from lib.db import get_db_connection
from models import StudyActivity, PaginatedStudySessions, StudyActivityCreate, PaginatedStudyActivities, PaginatedWords
from utils import paginate
from datetime import datetime
import json

router = APIRouter()

@router.get("/study_activities/{activity_id}", response_model=StudyActivity, tags=["Study Activities"])
def get_study_activity(activity_id: int = Path(..., title="The ID of the study activity to retrieve")):
    """
    Retrieve a study activity by its ID.

    - **activity_id**: The ID of the study activity to retrieve.
    """
    with get_db_connection() as conn:
        query = """
        SELECT sa.id, sa.name, sa.study_session_id, sa.group_id, sa.created_at,
               g.name as group_name,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = sa.study_session_id) as review_items_count
        FROM study_activities sa
        LEFT JOIN groups g ON g.id = sa.group_id
        WHERE sa.id = ?
        """
        cursor = conn.execute(query, (activity_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Study activity not found")
        
        # Convert row to StudyActivity model
        study_activity = StudyActivity(
            id=row[0],
            name=row[1],
            study_session_id=row[2],
            group_id=row[3],
            created_at=row[4],
            group_name=row[5],
            review_items_count=row[6]
        ).model_dump()
        
        return study_activity

@router.get("/study_activities/{activity_id}/study_sessions", response_model=PaginatedStudySessions, tags=["Study Activities"])
def get_activity_study_sessions(
    activity_id: int = Path(..., title="The ID of the study activity to retrieve study sessions for"),
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Retrieve a paginated list of study sessions for a specific study activity.

    - **activity_id**: The ID of the study activity to retrieve study sessions for.
    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # First check if the activity exists
        activity_exists = conn.execute(
            "SELECT 1 FROM study_activities WHERE id = ?", 
            (activity_id,)
        ).fetchone()
        
        if not activity_exists:
            raise HTTPException(status_code=404, detail="Study activity not found")

        # Query to get study sessions for the activity
        query = """
        SELECT ss.id,
               sa.name AS activity_name,
               g.name AS group_name,
               ss.created_at AS start_time,
               NULL AS end_time,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = ss.id) as review_items_count
        FROM study_sessions ss
        JOIN study_activities sa ON sa.study_session_id = ss.id
        LEFT JOIN groups g ON g.id = ss.group_id
        WHERE sa.id = ?
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query, (activity_id,))
        rows = cursor.fetchall()
        
        if not rows:
            raise HTTPException(
                status_code=404, 
                detail="No study sessions found for this activity"
            )
        
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

        # Get total count for pagination
        total_items = conn.execute(
            """
            SELECT COUNT(*) 
            FROM study_sessions ss
            JOIN study_activities sa ON sa.study_session_id = ss.id
            WHERE sa.id = ?
            """, 
            (activity_id,)
        ).fetchone()[0]
        
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

@router.post("/study_activities", response_model=StudyActivity, tags=["Study Activities"])
def create_study_activity(activity: StudyActivityCreate = Body(...)):
    """
    Create a new study activity and start a session.

    - **name**: The name of the study activity
    - **group_id**: The ID of the group this activity belongs to
    """
    with get_db_connection() as conn:
        # First check if the group exists
        group_exists = conn.execute(
            "SELECT 1 FROM groups WHERE id = ?", 
            (activity.group_id,)
        ).fetchone()
        
        if not group_exists:
            raise HTTPException(status_code=404, detail="Group not found")

        current_time = datetime.now().isoformat()

        # First create the study activity
        cursor = conn.execute(
            """
            INSERT INTO study_activities (name, group_id, created_at)
            VALUES (?, ?, ?)
            """,
            (activity.name, activity.group_id, current_time)
        )
        activity_id = cursor.lastrowid

        # Then create the study session with the activity_id
        cursor = conn.execute(
            """
            INSERT INTO study_sessions (group_id, study_activity_id, created_at) 
            VALUES (?, ?, ?)
            """,
            (activity.group_id, activity_id, current_time)
        )
        study_session_id = cursor.lastrowid

        # Update the study activity with the session ID
        cursor = conn.execute(
            """
            UPDATE study_activities 
            SET study_session_id = ? 
            WHERE id = ?
            """,
            (study_session_id, activity_id)
        )

        # Retrieve the created activity
        query = """
        SELECT sa.id, sa.name, sa.study_session_id, sa.group_id, sa.created_at,
               g.name as group_name,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = sa.study_session_id) as review_items_count
        FROM study_activities sa
        LEFT JOIN groups g ON g.id = sa.group_id
        WHERE sa.id = ?
        """
        cursor = conn.execute(query, (activity_id,))
        row = cursor.fetchone()
        
        # Convert row to StudyActivity model
        study_activity = StudyActivity(
            id=row[0],
            name=row[1],
            study_session_id=row[2],
            group_id=row[3],
            created_at=row[4],
            group_name=row[5],
            review_items_count=row[6]
        ).model_dump()
        
        return study_activity

@router.get("/study_activities", response_model=PaginatedStudyActivities, tags=["Study Activities"])
def get_study_activities(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Retrieve a paginated list of study activities.

    - **page**: The page number to retrieve (default: 1)
    - **page_size**: The number of items per page (default: 10)
    """
    with get_db_connection() as conn:
        # Base query
        query = """
        SELECT sa.id, sa.name, sa.study_session_id, sa.group_id, sa.created_at,
               g.name as group_name,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = sa.study_session_id) as review_items_count
        FROM study_activities sa
        LEFT JOIN groups g ON g.id = sa.group_id
        ORDER BY sa.created_at DESC
        """
        
        # Apply pagination
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query)
        rows = cursor.fetchall()
        
        # Convert rows to list of activities
        activities = [
            {
                "id": row[0],
                "name": row[1],
                "study_session_id": row[2],
                "group_id": row[3],
                "created_at": row[4],
                "group_name": row[5],
                "review_items_count": row[6]
            }
            for row in rows
        ]

        # Get total count for pagination
        total_items = conn.execute("SELECT COUNT(*) FROM study_activities").fetchone()[0]
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            "study_activities": activities,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "items_per_page": page_size
            }
        }

@router.get("/study_activities/{activity_id}/words", response_model=PaginatedWords, tags=["Study Activities"])
def get_activity_words(
    activity_id: int = Path(..., title="The ID of the study activity to retrieve words for"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Retrieve a paginated list of words for a specific study activity.

    - **activity_id**: The ID of the study activity to retrieve words for
    - **page**: The page number to retrieve (default: 1)
    - **page_size**: The number of items per page (default: 10)
    """
    with get_db_connection() as conn:
        # First check if the activity exists
        activity = conn.execute(
            "SELECT group_id FROM study_activities WHERE id = ?",
            (activity_id,)
        ).fetchone()

        if not activity:
            raise HTTPException(status_code=404, detail="Study activity not found")

        group_id = activity[0]

        # Get words for the group
        query = """
        SELECT w.id, w.jamaican_patois, w.english, w.parts,
               COALESCE(SUM(CASE WHEN wr.correct THEN 1 ELSE 0 END), 0) as correct_count,
               COALESCE(SUM(CASE WHEN NOT wr.correct THEN 1 ELSE 0 END), 0) as wrong_count
        FROM words w
        JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        WHERE wg.group_id = ?
        GROUP BY w.id
        """
        
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query, (group_id,))
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No words found for this activity"
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
            }
            for row in rows
        ]

        # Get total count for pagination
        total_items = conn.execute(
            """
            SELECT COUNT(DISTINCT w.id)
            FROM words w
            JOIN word_groups wg ON w.id = wg.word_id
            WHERE wg.group_id = ?
            """,
            (group_id,)
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