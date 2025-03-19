from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class SongSearchResult(BaseModel):
    """Schema for song search results"""
    title: str = Field(..., description="Title of the song")
    lyrics: str = Field(..., description="Full lyrics of the song")
    language: str = Field(..., description="Language of the song")
    artist: str = Field(..., description="Artist who performed the song")
    album: Optional[str] = Field(None, description="Album containing the song")
    release_date: Optional[str] = Field(None, description="Release date of the song")

class VocabularyItem(BaseModel):
    """Schema for vocabulary items"""
    word: str = Field(..., description="The vocabulary word or phrase")
    explanation: str = Field(..., description="Detailed explanation of the word/phrase")
    example_sentences: List[str] = Field(
        ..., 
        description="Example sentences using the word/phrase"
    )

class VocabularyRequest(BaseModel):
    """Schema for vocabulary generation request"""
    lyrics: str = Field(..., description="Song lyrics to extract vocabulary from")
    source_language: str = Field(..., description="Language of the lyrics")
    target_language: str = Field(..., description="Language of the learner")
    num_words: int = Field(default=30, description="Number of vocabulary items to generate") 