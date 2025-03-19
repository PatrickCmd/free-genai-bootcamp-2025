import os
import json
from typing import List
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from .schemas import VocabularyItem, VocabularyRequest

# Load environment variables
_ = load_dotenv(find_dotenv())


class VocabularyGenerator:
    """Agent for generating vocabulary from song lyrics"""
    
    def __init__(self):
        """Initialize the vocabulary generator with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    async def generate_vocabulary(self, request: VocabularyRequest) -> List[VocabularyItem]:
        """
        Generate vocabulary items from song lyrics
        
        Args:
            request: VocabularyRequest containing lyrics and language info
            
        Returns:
            List of VocabularyItem objects
        """
        try:
            # Use the OpenAI responses API for vocabulary generation
            messages = [
                {
                    "role": "developer",
                    "content": (
                        f"You are a language learning expert specializing in {request.source_language}. "
                        f"Extract useful vocabulary from the provided song lyrics. "
                        f"For each vocabulary item, provide: "
                        f"1. The word or phrase in {request.source_language} "
                        f"2. A clear explanation in {request.target_language} "
                        f"3. 2-3 example sentences showing usage in {request.source_language} "
                        f"Choose vocabulary that would be valuable for a language learner. "
                        f"Focus on words that are common and useful but might be challenging for learners."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Please extract and explain atleast {request.num_words} vocabulary items from these "
                        f"{request.source_language} song lyrics:\n\n{request.lyrics}"
                    )
                }
            ]
            
            response = self.client.responses.create(
                model="gpt-4o",
                input=messages,
                temperature=0.0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "vocabulary_generation",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "vocabulary_items": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "word": {"type": "string"},
                                            "explanation": {"type": "string"},
                                            "example_sentences": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            }
                                        },
                                        "required": ["word", "explanation", "example_sentences"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["vocabulary_items"],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )

            # Convert response to VocabularyItem objects
            result_dict = json.loads(response.output_text)
            return [VocabularyItem.model_validate(item) for item in result_dict["vocabulary_items"]]

        except Exception as e:
            print(f"Error generating vocabulary: {e}")
            return [] 