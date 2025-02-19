import json
from fastapi import APIRouter, HTTPException, Query
from lib.db import get_db_connection
from utils import paginate
from models import PaginatedWords, Word

router = APIRouter()

@router.get("/words", response_model=PaginatedWords, tags=["Words"])
def get_words(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    """
    Retrieve a paginated list of words.

    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    """
    with get_db_connection() as conn:
        # Query to get words with correct and wrong counts
        query = """
        SELECT w.id, w.jamaican_patois, w.english, w.parts,
               COALESCE(SUM(CASE WHEN wr.correct THEN 1 ELSE 0 END), 0) AS correct_count,
               COALESCE(SUM(CASE WHEN NOT wr.correct THEN 1 ELSE 0 END), 0) AS wrong_count
        FROM words w
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        GROUP BY w.id
        """
        paginated_query = paginate(query, page, page_size)
        cursor = conn.execute(paginated_query)
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No words found")
        
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
        total_items = conn.execute("SELECT COUNT(*) FROM words").fetchone()[0]
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