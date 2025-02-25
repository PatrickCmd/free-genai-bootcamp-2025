import json
import os
from datetime import datetime
from .schema import validate_words, validate_groups, validate_word_groups
from utils.helpers import assign_ids, slugify

def export_words(words, filename=None, theme=None):
    """
    Export words to a JSON file
    
    Args:
        words (list): List of word dictionaries
        filename (str, optional): Output filename. If None, a default name is generated.
        theme (str, optional): Theme/category name to include in the filename.
        
    Returns:
        str: Path to the exported file
    """
    # Validate words
    try:
        validated_words = validate_words(words)
        
        # Convert to dictionaries
        word_dicts = [word.model_dump() for word in validated_words]
    except Exception as e:
        # If validation fails, use the original words
        word_dicts = words
    
    # Ensure all words have an ID
    for word in word_dicts:
        if 'id' not in word or word['id'] is None:
            word['id'] = 0
    
    # Assign IDs if not present
    max_id = 0
    for word in word_dicts:
        if word.get('id') is not None and word.get('id') > max_id:
            max_id = word.get('id')
    
    for i, word in enumerate(word_dicts):
        if word.get('id') is None or word.get('id') == 0:
            word['id'] = max_id + i + 1
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        theme_slug = slugify(theme) if theme else "words"
        filename = f"{theme_slug}_words_{timestamp}.json"
    
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
    group = {"id": 1, "name": name}
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        theme_slug = slugify(name)
        filename = f"{theme_slug}_group_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump([group], f, indent=2)
    
    return filepath

def export_word_groups(word_ids, group_id, filename=None, theme=None):
    """
    Export word-group associations to a JSON file
    
    Args:
        word_ids (list): List of word IDs
        group_id (int): Group ID
        filename (str, optional): Output filename. If None, a default name is generated.
        theme (str, optional): Theme/category name to include in the filename.
        
    Returns:
        str: Path to the exported file
    """
    # Ensure we have valid word IDs
    if not word_ids:
        word_ids = [1]  # Default to at least one word ID
    
    associations = [{"word_id": word_id, "group_id": group_id} for word_id in word_ids]
    
    # Assign IDs
    for i, assoc in enumerate(associations):
        assoc['id'] = i + 1
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        theme_slug = slugify(theme) if theme else "associations"
        filename = f"{theme_slug}_word_groups_{timestamp}.json"
    
    # Ensure the exports directory exists
    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(associations, f, indent=2)
    
    return filepath 