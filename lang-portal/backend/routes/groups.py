from fastapi import APIRouter, HTTPException, Query, Path
from lib.db import get_db_connection
from utils import paginate
from models import PaginatedGroups, Group, PaginatedWords, Word, PaginatedStudySessions, StudySession
import json

router = APIRouter()

@router.get("/groups", response_model=PaginatedGroups, tags=["Groups"])
def get_groups(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of groups.

    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # Query to get groups with word count
        query = """
        SELECT g.id, g.name,
               (SELECT COUNT(*) FROM word_groups wg WHERE wg.group_id = g.id) as word_count
        FROM groups g
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query)
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No groups found")
        
        # Convert rows to list of Group models and then to dictionaries
        groups = [
            Group(
                id=row[0],
                name=row[1],
                word_count=row[2],
                description=None  # Assuming description is not part of the query
            ).model_dump() for row in rows
        ]

        # Calculate total items and total pages
        total_items = conn.execute("SELECT COUNT(*) FROM groups").fetchone()[0]
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            "groups": groups,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items,
                "items_per_page": page_size
            }
        }

@router.get("/groups/{group_id}", response_model=Group, tags=["Groups"])
def get_group(group_id: int = Path(..., title="The ID of the group to retrieve")):
    """
    Retrieve a group by its ID.

    - **group_id**: The ID of the group to retrieve.
    """
    with get_db_connection() as conn:
        query = """
        SELECT g.id, g.name,
               (SELECT COUNT(*) FROM word_groups wg WHERE wg.group_id = g.id) as word_count
        FROM groups g
        WHERE g.id = ?
        """
        cursor = conn.execute(query, (group_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Convert row to Group model
        group = Group(
            id=row[0],
            name=row[1],
            word_count=row[2],
            description=None  # Assuming description is not part of the query
        ).model_dump()
        
        return group

@router.get("/groups/{group_id}/words", response_model=PaginatedWords, tags=["Groups"])
def get_group_words(group_id: int = Path(..., title="The ID of the group to retrieve words for"),
                    page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of words for a specific group.

    - **group_id**: The ID of the group to retrieve words for.
    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # Query to get words for a specific group
        query = """
        SELECT w.id, w.jamaican_patois, w.english, w.parts,
               COALESCE(SUM(CASE WHEN wr.correct THEN 1 ELSE 0 END), 0) AS correct_count,
               COALESCE(SUM(CASE WHEN NOT wr.correct THEN 1 ELSE 0 END), 0) AS wrong_count
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
            raise HTTPException(status_code=404, detail="No words found for this group")
        
        # Convert rows to list of Word models and then to dictionaries
        words = [
            Word(
                id=row[0],
                jamaican_patois=row[1],
                english=row[2],
                parts=json.loads(row[3]) if row[3] else None,
                correct_count=row[4],
                wrong_count=row[5]
            ).model_dump() for row in rows
        ]

        # Calculate total items and total pages
        total_items = conn.execute("SELECT COUNT(*) FROM word_groups WHERE group_id = ?", (group_id,)).fetchone()[0]
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

@router.get("/groups/{group_id}/study_sessions", response_model=PaginatedStudySessions, tags=["Groups"])
def get_group_study_sessions(group_id: int = Path(..., title="The ID of the group to retrieve study sessions for"),
                             page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of study sessions for a specific group.

    - **group_id**: The ID of the group to retrieve study sessions for.
    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # Query to get study sessions for a specific group
        query = """
        SELECT ss.id,
               sa.name AS activity_name,
               g.name AS group_name,
               ss.created_at AS start_time,
               NULL AS end_time,  -- or if you store an end_time, select it
               (SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) as review_items_count
        FROM study_sessions ss
        LEFT JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN groups g ON g.id = ss.group_id
        WHERE ss.group_id = ?
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query, (group_id,))
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No study sessions found for this group")
        
        # Convert rows to list of StudySession models and then to dictionaries
        study_sessions = [
            StudySession(
                id=row[0],
                activity_name=row[1],
                group_name=row[2],
                start_time=row[3],
                end_time=row[4],
                review_items_count=row[5]
            ).model_dump() for row in rows
        ]

        # Calculate total items and total pages
        total_items = conn.execute("SELECT COUNT(*) FROM study_sessions WHERE group_id = ?", (group_id,)).fetchone()[0]
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