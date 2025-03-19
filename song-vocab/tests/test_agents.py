import os
import sys
from pathlib import Path
import pytest
from datetime import date

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from agents.web_search import WebSearchAgent
from agents.vocab_gen import VocabularyGenerator
from agents.schemas import VocabularyRequest

@pytest.mark.asyncio
async def test_web_search():
    """Test web search agent"""
    agent = WebSearchAgent()
    
    # Test parameters
    title = "Settle Down"
    user_language = "English"
    foreign_language = "Jamaican Patois"
    
    result = await agent.search_song(
        title=title,
        user_language=user_language,
        foreign_language=foreign_language
    )
    
    assert result is not None
    assert result.title == title
    assert result.language == foreign_language
    
    print("\nWeb Search Results:")
    print(f"Title: {result.title}")
    print(f"Artist: {result.artist}")
    print(f"Album: {result.album or 'N/A'}")
    print(f"Language: {result.language}")
    print(f"Release Date: {result.release_date or 'N/A'}")
    print(f"Lyrics preview: {result.lyrics[:100]}...")

@pytest.mark.asyncio
async def test_vocab_generation():
    """Test vocabulary generation"""
    generator = VocabularyGenerator()
    request = VocabularyRequest(
        lyrics="Mi love when yuh wine up yuh body pon mi\nGyal yuh look good and yuh know yuh sweet...",
        source_language="Jamaican Patois",
        target_language="English",
        num_words=3
    )
    
    vocab_items = await generator.generate_vocabulary(request)
    
    assert len(vocab_items) > 0
    print("\nVocabulary Generation Results:")
    for item in vocab_items:
        print(f"\nWord: {item.word}")
        print(f"Explanation: {item.explanation}")
        print("Example sentences:")
        for sentence in item.example_sentences:
            print(f"- {sentence}")

if __name__ == "__main__":
    pytest.main([__file__]) 