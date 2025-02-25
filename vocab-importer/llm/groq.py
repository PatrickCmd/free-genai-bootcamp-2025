import os
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client():
    """
    Initialize and return a Groq client
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    
    return groq.Groq(api_key=api_key)

def generate_vocabulary(theme, count, model="llama-3-70b", temperature=0.7, max_tokens=2000):
    """
    Generate vocabulary items using Groq models
    
    Args:
        theme (str): The theme or category for vocabulary generation
        count (int): Number of vocabulary items to generate
        model (str): Groq model to use
        temperature (float): Creativity parameter (0.0 to 1.0)
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        list: List of vocabulary items
    """
    client = get_client()
    
    prompt = f"""
    You are a language expert specializing in Jamaican Patois. Your task is to generate vocabulary items for learning Jamaican Patois based on the theme: {theme}.

    For each vocabulary item, provide:
    1. The Jamaican Patois word or phrase
    2. The English translation
    3. Part of speech (noun, verb, adjective, phrase, etc.)
    4. (Optional) Usage notes or context

    Generate {count} vocabulary items that are authentic, commonly used, and appropriate for language learners.

    Format your response as a JSON array with the following structure for each item:
    {{
      "jamaican_patois": "word/phrase",
      "english": "translation",
      "parts": {{
        "type": "part of speech",
        "usage": "usage notes (optional)"
      }}
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
            max_tokens=max_tokens
        )
        
        # Extract and parse the JSON response
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Error generating vocabulary with Groq: {str(e)}") 