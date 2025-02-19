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

class StudySession(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: Optional[str]
    review_items_count: int

class PaginatedWords(BaseModel):
    words: List[Word]
    pagination: dict

class PaginatedGroups(BaseModel):
    groups: List[Group]
    pagination: dict

class PaginatedStudySessions(BaseModel):
    study_sessions: List[StudySession]
    pagination: dict 