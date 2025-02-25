import json
import os
from datetime import datetime
from utils.helpers import generate_timestamp

# Path to store feedback data
FEEDBACK_FILE = "feedback_data.json"

def save_feedback(theme, llm_provider, llm_model, rating, comment, word_count):
    """
    Save feedback to a JSON file
    
    Args:
        theme (str): The theme/category of the vocabulary
        llm_provider (str): The LLM provider used
        llm_model (str): The specific model used
        rating (int): Rating from 1-5
        comment (str): Optional comment
        word_count (int): Number of words generated
        
    Returns:
        bool: True if successful, False otherwise
    """
    feedback_item = {
        "id": None,  # Will be assigned when saving
        "timestamp": generate_timestamp(),
        "theme": theme,
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "rating": rating,
        "comment": comment,
        "word_count": word_count
    }
    
    try:
        # Load existing feedback if file exists
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r') as f:
                feedback_data = json.load(f)
        else:
            feedback_data = []
        
        # Assign ID
        if feedback_data:
            max_id = max(item["id"] for item in feedback_data if item["id"] is not None)
            feedback_item["id"] = max_id + 1
        else:
            feedback_item["id"] = 1
        
        # Add new feedback and save
        feedback_data.append(feedback_item)
        
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error saving feedback: {str(e)}")
        return False

def get_all_feedback():
    """
    Get all saved feedback
    
    Returns:
        list: List of feedback items
    """
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return [] 