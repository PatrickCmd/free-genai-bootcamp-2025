from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class WordParts(BaseModel):
    type: str
    usage: Optional[str] = None

class Word(BaseModel):
    id: Optional[int] = None
    jamaican_patois: str
    english: str
    parts: WordParts

class Group(BaseModel):
    id: Optional[int] = None
    name: str

class WordGroup(BaseModel):
    id: Optional[int] = None
    word_id: int
    group_id: int

class Feedback(BaseModel):
    id: Optional[int] = None
    timestamp: str
    theme: str
    llm_provider: str
    llm_model: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    word_count: int

def validate_words(data: List[Dict]) -> List[Word]:
    """
    Validate a list of word dictionaries against the Word schema
    
    Args:
        data (List[Dict]): List of word dictionaries
        
    Returns:
        List[Word]: List of validated Word objects
    """
    return [Word(**item) for item in data]

def validate_groups(data: List[Dict]) -> List[Group]:
    """
    Validate a list of group dictionaries against the Group schema
    
    Args:
        data (List[Dict]): List of group dictionaries
        
    Returns:
        List[Group]: List of validated Group objects
    """
    return [Group(**item) for item in data]

def validate_word_groups(data: List[Dict]) -> List[WordGroup]:
    """
    Validate a list of word-group association dictionaries against the WordGroup schema
    
    Args:
        data (List[Dict]): List of word-group association dictionaries
        
    Returns:
        List[WordGroup]: List of validated WordGroup objects
    """
    return [WordGroup(**item) for item in data] 