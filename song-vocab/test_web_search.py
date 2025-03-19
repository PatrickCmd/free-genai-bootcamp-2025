import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

user_language = "English"
foreign_language = "Jamaican Patois"
song_title = "Mavado - Settle Down"
messages = [
    {
        "role": "developer",
        "content": f"""
You are a helpful language tutor. 
When the user provides a song title, search for the song lyrics and help them learn new vocabulary from it. 
First search for the lyrics, then extract vocabulary from them (atleast 30 vocabularies). 
Explain the meaning of new words in simple terms and provide example sentences. 
Use the user's native language to explain the meaning of new words.
Focus on words that would be valuable for a language learner.
The user's native language is {user_language}.
The language of the foreign song the user is learning is {foreign_language}.
        """,
    },
    {
        "role": "user",
        "content": f"help me learn about the song '{song_title}'",
    },
]

response = client.responses.create(
    model="gpt-4o",  # or another supported model
    input=messages,
    tools=[
        {
            "type": "web_search"
        }
    ],
    temperature=0.0,
    text={
        "format": {
            "type": "json_schema",
            "name": "song_vocab_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "song_title": { "type": "string" },
                    # "song_lyrics": { "type": "string" },
                    "vocabs": { 
                        "type": "array",
                        "items": { "type": "string" }
                    },
                    "vocab_explanations": { "type": "array", "items": { "type": "string" } },
                    "example_sentences": { "type": "array", "items": { "type": "string" } }
                },
                "required": ["song_title", "vocabs", "vocab_explanations", "example_sentences"],
                "additionalProperties": False
            },
            "strict": True
        },
    },
)

# print(response.output_text)

song_vocab_extraction = json.loads(response.output_text)

print(song_vocab_extraction)

# Save the response to a file
with open('song_vocab_extraction.json', 'w') as f:
    json.dump(song_vocab_extraction, f)

print("Response saved to song_vocab_extraction.json")
