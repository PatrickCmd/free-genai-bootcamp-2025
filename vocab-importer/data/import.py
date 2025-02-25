import json
from .schema import validate_words, validate_groups, validate_word_groups

def import_words(file_content):
    """
    Import words from a JSON file
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (validated_words, errors)
    """
    try:
        data = json.loads(file_content)
        validated_words = validate_words(data)
        return validated_words, None
    except Exception as e:
        return None, str(e)

def import_groups(file_content):
    """
    Import groups from a JSON file
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (validated_groups, errors)
    """
    try:
        data = json.loads(file_content)
        validated_groups = validate_groups(data)
        return validated_groups, None
    except Exception as e:
        return None, str(e)

def import_word_groups(file_content):
    """
    Import word-group associations from a JSON file
    
    Args:
        file_content (str): JSON file content
        
    Returns:
        tuple: (validated_word_groups, errors)
    """
    try:
        data = json.loads(file_content)
        validated_word_groups = validate_word_groups(data)
        return validated_word_groups, None
    except Exception as e:
        return None, str(e) 