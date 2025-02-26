import json
import os
from datetime import datetime
from .schema import validate_words, validate_groups, validate_word_groups
from utils.helpers import assign_ids, slugify
from .database import (
    get_group_id, 
    get_last_group_id, 
    get_last_word_id, 
    get_last_word_group_id,
    check_database_exists
)

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
    
    # Get the last word ID from the database if it exists
    last_id = 0
    if check_database_exists():
        try:
            last_id = get_last_word_id()
            print(f"Last word ID in database: {last_id}")
        except Exception as e:
            print(f"Error getting last word ID: {str(e)}")
    
    # Ensure all words have an ID
    for word in word_dicts:
        if 'id' not in word or word['id'] is None:
            word['id'] = 0
    
    # Assign IDs if not present, starting after the last ID in the database
    for i, word in enumerate(word_dicts):
        if word.get('id') is None or word.get('id') == 0:
            word['id'] = last_id + i + 1
    
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
    # Check if the group already exists in the database
    group_id = None
    if check_database_exists():
        try:
            group_id = get_group_id(name)
            if group_id:
                print(f"Group '{name}' already exists with ID: {group_id}")
            else:
                # Get the last group ID and increment
                last_id = get_last_group_id()
                group_id = last_id + 1
                print(f"Creating new group ID: {group_id}")
        except Exception as e:
            print(f"Error checking group: {str(e)}")
            # Default to ID 1 if there's an error
            group_id = 1
    else:
        # Default to ID 1 if database doesn't exist
        group_id = 1
    
    group = {"id": group_id, "name": name}
    
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
    
    # Get the last word_group ID from the database if it exists
    last_id = 0
    if check_database_exists():
        try:
            last_id = get_last_word_group_id()
            print(f"Last word_group ID in database: {last_id}")
        except Exception as e:
            print(f"Error getting last word_group ID: {str(e)}")
    
    # Assign IDs starting after the last ID in the database
    for i, assoc in enumerate(associations):
        assoc['id'] = last_id + i + 1
    
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