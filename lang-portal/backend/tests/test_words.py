import sys
import os
import pytest
from fastapi.testclient import TestClient
# Add the backend directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.append(backend_dir)

from app import app

client = TestClient(app)

def test_get_words():
    response = client.get("/api/words")
    assert response.status_code == 200
    assert "words" in response.json()
    assert "pagination" in response.json()
    assert "current_page" in response.json()["pagination"]
    assert "total_pages" in response.json()["pagination"]
    assert "total_items" in response.json()["pagination"]
    assert "items_per_page" in response.json()["pagination"]

def test_get_words_with_pagination():
    response = client.get("/api/words?page=2&page_size=5")
    assert response.status_code == 200
    assert "words" in response.json()
    assert response.json()["pagination"]["current_page"] == 2
    assert response.json()["pagination"]["items_per_page"] == 5

def test_get_word():
    response = client.get("/api/words/1")
    assert response.status_code == 200
    word = response.json()
    assert "id" in word
    assert "jamaican_patois" in word
    assert "english" in word
    assert "parts" in word
    assert "correct_count" in word
    assert "wrong_count" in word

def test_get_word_not_found():
    response = client.get("/api/words/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"

def test_get_word_groups():
    response = client.get("/api/words/1/groups")
    assert response.status_code == 200
    data = response.json()
    assert "groups" in data
    assert "pagination" in data
    
    if len(data["groups"]) > 0:
        group = data["groups"][0]
        assert "id" in group
        assert "name" in group
        assert "word_count" in group

def test_get_word_groups_not_found():
    response = client.get("/api/words/9999/groups")
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found" 