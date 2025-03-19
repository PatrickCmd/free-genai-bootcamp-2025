from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel, Field, field_validator

class SongBase(BaseModel):
    """Base model for song data"""
    title: str = Field(..., description="Title of the song")
    lyrics: str = Field(..., description="Lyrics of the song")
    language: str = Field(..., description="Language of the song")
    artist: str = Field(..., description="Artist who performed the song")
    album: Optional[str] = Field(None, description="Album containing the song")
    release_date: Optional[str] = Field(None, description="Release date of the song")

class Song(SongBase):
    """Song model with ID"""
    id: int = Field(..., description="Unique identifier for the song")

class VocabularyBase(BaseModel):
    """Base model for vocabulary data"""
    song_id: Optional[int] = None
    word: str = Field(..., description="The vocabulary word or phrase")
    explanation: str = Field(..., description="Explanation or definition of the vocabulary")
    example_sentences: Union[str, List[str]]
    
    @field_validator('example_sentences')
    def validate_example_sentences(cls, v):
        """Convert example_sentences to string if it's a list"""
        if isinstance(v, list):
            return "|||".join(v)
        return v

class Vocabulary(VocabularyBase):
    """Vocabulary model with ID"""
    id: int = Field(..., description="Unique identifier for the vocabulary entry") 