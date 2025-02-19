from pydantic import BaseModel
from typing import List, Optional

class Word(BaseModel):
    id: int
    jamaican_patois: str
    english: str
    parts: Optional[dict]
    correct_count: int
    wrong_count: int

class Group(BaseModel):
    id: int
    name: str
    word_count: int
    description: Optional[str]

class PaginatedWords(BaseModel):
    words: List[Word]
    pagination: dict

class PaginatedGroups(BaseModel):
    groups: List[Group]
    pagination: dict 