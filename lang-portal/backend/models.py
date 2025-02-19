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

class StudyActivity(BaseModel):
    id: int
    name: str
    study_session_id: Optional[int]
    group_id: Optional[int]
    created_at: str
    group_name: Optional[str]
    review_items_count: int

class StudyActivityCreate(BaseModel):
    name: str
    group_id: int

class WordReview(BaseModel):
    id: int
    word_id: int
    study_session_id: int
    correct: bool
    created_at: str
    word_jamaican_patois: str
    word_english: str

class StudyProgress(BaseModel):
    total_words_reviewed: int
    total_correct: int
    total_incorrect: int
    accuracy_rate: float
    total_study_sessions: int
    total_study_time_minutes: int
    words_by_group: List[dict]

class QuickStats(BaseModel):
    total_words: int
    words_learned: int  # Words with at least one correct review
    total_study_time_minutes: int
    recent_accuracy: float  # Accuracy rate for last 50 reviews
    streak_days: int  # Consecutive days with study sessions 