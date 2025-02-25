import json
import re
from datetime import datetime

def extract_json_from_text(text):
    """
    Extract JSON from text that might contain additional content
    
    Args:
        text (str): Text that might contain JSON
        
    Returns:
        dict or list: Parsed JSON data
    """
    # Try to find JSON array or object in the text
    json_match = re.search(r'(\[|\{).*(\]|\})', text, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If direct extraction fails, try to clean the string
            cleaned_json = re.sub(r'```json|```', '', json_str).strip()
            return json.loads(cleaned_json)
    
    # If no JSON-like structure is found, raise an error
    raise ValueError("No valid JSON found in the text")

def generate_timestamp():
    """
    Generate a current timestamp string
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().isoformat()

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