import json
import re
from datetime import datetime
import unicodedata

def extract_json_from_text(text):
    """
    Extract JSON from text that might contain additional content
    
    Args:
        text (str): Text that might contain JSON
        
    Returns:
        dict or list: Parsed JSON data
    """
    # If the text is already valid JSON, return it directly
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array or object in the text
    json_match = re.search(r'(\{|\[).*(\}|\])', text, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If direct extraction fails, try to clean the string
            cleaned_json = re.sub(r'```json|```', '', json_str).strip()
            try:
                return json.loads(cleaned_json)
            except json.JSONDecodeError:
                # If still fails, try to extract just the array part
                array_match = re.search(r'\[(.*)\]', cleaned_json, re.DOTALL)
                if array_match:
                    try:
                        return json.loads(array_match.group(0))
                    except:
                        pass
    
    # If no JSON-like structure is found, raise an error
    raise ValueError("No valid JSON found in the text")

def generate_timestamp():
    """
    Generate a current timestamp string
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def assign_ids(items, start_id=1):
    """
    Assign sequential IDs to a list of dictionaries
    
    Args:
        items (list): List of dictionaries
        start_id (int): Starting ID value
        
    Returns:
        list: List of dictionaries with IDs assigned
    """
    for i, item in enumerate(items):
        item['id'] = start_id + i
    return items

def slugify(text):
    """
    Convert text to a URL-friendly slug
    
    Args:
        text (str): Text to slugify
        
    Returns:
        str: Slugified text
    """
    # Convert to lowercase and normalize unicode characters
    text = unicodedata.normalize('NFKD', text.lower())
    
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    # Limit length
    if len(text) > 50:
        text = text[:50]
    
    # Ensure we have a valid slug
    if not text:
        text = 'unnamed'
    
    return text 