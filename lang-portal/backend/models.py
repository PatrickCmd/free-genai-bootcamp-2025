from pydantic import BaseModel
from typing import List, Optional

class Word(BaseModel):
    id: int
    jamaican_patois: str
    english: str
    parts: Optional[dict]
    correct_count: int
    wrong_count: int

class PaginatedWords(BaseModel):
    words: List[Word]
    pagination: dict 