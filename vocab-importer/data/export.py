import json
import os
from datetime import datetime
from .schema import validate_words, validate_groups, validate_word_groups
from utils.helpers import assign_ids

def export_words(words, filename=None):
    """
    Export words to a JSON file
    
    Args:
        words (list): List of word dictionaries
        filename (str, optional): Output filename. If None, a default name is generated.
        
    Returns:
        str: Path to the exported file
    """
    # Validate words
    validated_words = validate_words(words)
    
    # Convert to dictionaries
    word_dicts = [word.model_dump() for word in validated_words]
    
    # Assign IDs if not present
    word_dicts = assign_ids([w for w in word_dicts if w.get('id') is None], 
                           start_id=max([w.get('id', 0) for w in word_dicts], default=0) + 1)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"words_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(word_dicts, f, indent=2)
    
    return filepath

def export_group(name, filename=None):
    """
    Export a group to a JSON file
    
    Args:
        name (str): Group name
        filename (str, optional): Output filename. If None, a default name is generated.
        
    Returns:
        str: Path to the exported file
    """
    group = {"name": name}
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"group_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump([group], f, indent=2)
    
    return filepath

def export_word_groups(word_ids, group_id, filename=None):
    """
    Export word-group associations to a JSON file
    
    Args:
        word_ids (list): List of word IDs
        group_id (int): Group ID
        filename (str, optional): Output filename. If None, a default name is generated.
        
    Returns:
        str: Path to the exported file
    """
    associations = [{"word_id": word_id, "group_id": group_id} for word_id in word_ids]
    
    # Assign IDs
    associations = assign_ids(associations)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"word_groups_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(associations, f, indent=2)
    
    return filepath 