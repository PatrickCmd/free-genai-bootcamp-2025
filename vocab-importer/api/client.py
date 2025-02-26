import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API URL from environment or use default
API_URL = os.getenv("API_URL", "http://localhost:8000/api")
API_KEY = os.getenv("API_KEY", "")

def check_api_connection():
    """
    Check if the backend API is accessible
    
    Returns:
        bool: True if connected, False otherwise
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def get_headers():
    """
    Get headers for API requests
    
    Returns:
        dict: Headers including API key if available
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    return headers

def sync_words(words):
    """
    Sync words with the backend API
    
    Args:
        words (list): List of word dictionaries
        
    Returns:
        tuple: (success, message)
    """
    try:
        response = requests.post(
            f"{API_URL}/words/sync",
            headers=get_headers(),
            json={"words": words}
        )
        
        if response.status_code in (200, 201):
            return True, f"Successfully synced {len(words)} words"
        else:
            return False, f"Error syncing words: {response.text}"
    except Exception as e:
        return False, f"Error connecting to API: {str(e)}"

def sync_groups(groups):
    """
    Sync groups with the backend API
    
    Args:
        groups (list): List of group dictionaries
        
    Returns:
        tuple: (success, message)
    """
    try:
        response = requests.post(
            f"{API_URL}/groups/sync",
            headers=get_headers(),
            json={"groups": groups}
        )
        
        if response.status_code in (200, 201):
            return True, f"Successfully synced {len(groups)} groups"
        else:
            return False, f"Error syncing groups: {response.text}"
    except Exception as e:
        return False, f"Error connecting to API: {str(e)}"

def sync_word_groups(word_groups):
    """
    Sync word-group associations with the backend API
    
    Args:
        word_groups (list): List of word-group association dictionaries
        
    Returns:
        tuple: (success, message)
    """
    try:
        response = requests.post(
            f"{API_URL}/word-groups/sync",
            headers=get_headers(),
            json={"word_groups": word_groups}
        )
        
        if response.status_code in (200, 201):
            return True, f"Successfully synced {len(word_groups)} associations"
        else:
            return False, f"Error syncing associations: {response.text}"
    except Exception as e:
        return False, f"Error connecting to API: {str(e)}"

def get_all_groups():
    """
    Get all groups from the backend API
    
    Returns:
        tuple: (groups, error)
    """
    try:
        response = requests.get(
            f"{API_URL}/groups",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error fetching groups: {response.text}"
    except Exception as e:
        return None, f"Error connecting to API: {str(e)}"

def get_words_by_group(group_id):
    """
    Get words by group ID from the backend API
    
    Args:
        group_id (int): Group ID
        
    Returns:
        tuple: (words, error)
    """
    try:
        response = requests.get(
            f"{API_URL}/groups/{group_id}/words",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error fetching words: {response.text}"
    except Exception as e:
        return None, f"Error connecting to API: {str(e)}" 