from fastapi import APIRouter, HTTPException, Query, Path
from lib.db import get_db_connection
from utils import paginate
from models import PaginatedGroups, Group

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