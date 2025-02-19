from fastapi import Query

def paginate(query, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    offset = (page - 1) * page_size
    paginated_query = f"{query} LIMIT {page_size} OFFSET {offset}"
    return paginated_query 