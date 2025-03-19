import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from .schemas import SongSearchResult
from datetime import datetime

# Load environment variables
_ = load_dotenv(find_dotenv())

class WebSearchAgent:
    """Agent for searching song lyrics using web search"""
    
    def __init__(self):
        """Initialize the web search agent with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    async def search_song(self, title: str, user_language: str, foreign_language: str) -> Optional[SongSearchResult]:
        """
        Search for song lyrics and details using web search
        
        Args:
            title: The title of the song to search for
            user_language: The language the user understands
            foreign_language: The language of the song
            
        Returns:
            SongSearchResult object or None if search fails
        """
        try:
            # Use the OpenAI responses API with web search tool
            messages = [
                {
                    "role": "developer",
                    "content": (
                        f"You are a helpful language tutor. "
                        f"When the user provides a song title, search for the song lyrics and help them learn new vocabulary from it. "
                        f"First search for the lyrics with proper formatting, then extract information about the song. "
                        f"The user's native language is {user_language}. "
                        f"The language of the foreign song the user is learning is {foreign_language}. "
                    )
                },
                {
                    "role": "user",
                    "content": f"Help me find the lyrics and information for the song '{title}' in {foreign_language}"
                }
            ]
            
            response = self.client.responses.create(
                model="gpt-4o",
                input=messages,
                tools=[{"type": "web_search"}],
                temperature=0.0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "song_search_result",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "lyrics": {"type": "string"},
                                "language": {"type": "string"},
                                "artist": {"type": "string"},
                                "album": {"type": "string"},
                                "release_date": {"type": "string"}
                            },
                            "required": ["title", "lyrics", "language", "artist", "album", "release_date"],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )

            # Convert response to SongSearchResult
            result_dict = response.output_text
            return SongSearchResult.model_validate_json(result_dict)

        except Exception as e:
            print(f"Error searching for song: {e}")
            return None 