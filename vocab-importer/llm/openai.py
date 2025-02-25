import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from utils.helpers import extract_json_from_text

# Load environment variables
load_dotenv()

def get_client():
    """
    Initialize and return an OpenAI client
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    
    return OpenAI(api_key=api_key)

def generate_vocabulary(theme, count, model="gpt-4o", temperature=0.7, max_tokens=2000):
    """
    Generate vocabulary items using OpenAI models
    
    Args:
        theme (str): The theme or category for vocabulary generation
        count (int): Number of vocabulary items to generate
        model (str): OpenAI model to use
        temperature (float): Creativity parameter (0.0 to 1.0)
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        str: JSON string containing vocabulary items
    """
    client = get_client()
    
    prompt = f"""
    You are a language expert specializing in Jamaican Patois. Your task is to generate vocabulary items for learning Jamaican Patois based on the theme: {theme}.

    For each vocabulary item, provide:
    1. The Jamaican Patois word or phrase
    2. The English translation
    3. Part of speech (noun, verb, adjective, phrase, etc.)
    4. (Optional) Usage notes or context

    Generate exactly {count} vocabulary items that are authentic, commonly used, and appropriate for language learners.

    Format your response as a JSON object with the following structure:
    {{
      "words": [
        {{
          "jamaican_patois": "word/phrase",
          "english": "translation",
          "parts": {{
            "type": "part of speech",
            "usage": "usage notes (optional)"
          }}
        }},
        // more items...
      ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Jamaican Patois language expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        print(f"OpenAI response: {content}")
        
        # Use the extract_json_from_text function to handle various response formats
        try:
            parsed_json = extract_json_from_text(content)
            
            # Check if the response has the expected structure
            if "words" in parsed_json and isinstance(parsed_json["words"], list):
                return content
            else:
                # If the structure is not as expected, try to fix it
                if isinstance(parsed_json, list):
                    # If it's a list, wrap it in the expected structure
                    return json.dumps({"words": parsed_json})
                elif isinstance(parsed_json, dict):
                    # If it's a dictionary but doesn't have 'words' key, add it
                    words_list = []
                    # Try to extract words from the dictionary
                    for key, value in parsed_json.items():
                        if isinstance(value, list):
                            words_list = value
                            break
                    
                    if not words_list:
                        # If we couldn't find a list, use the whole dict as a single item if it has the right keys
                        if "jamaican_patois" in parsed_json and "english" in parsed_json:
                            words_list = [parsed_json]
                    
                    return json.dumps({"words": words_list})
                else:
                    # If it's something else, create a valid but empty response
                    return json.dumps({"words": []})
                    
        except Exception as e:
            print(f"Error extracting JSON: {str(e)}")
            # If extraction fails, return a valid but empty response
            return json.dumps({"words": []})
        
    except Exception as e:
        raise Exception(f"Error generating vocabulary with OpenAI: {str(e)}") 