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

def test_get_study_sessions():
    response = client.get("/api/study_sessions")
    assert response.status_code == 200
    assert "study_sessions" in response.json()
    assert "pagination" in response.json()
    assert "current_page" in response.json()["pagination"]
    assert "total_pages" in response.json()["pagination"]
    assert "total_items" in response.json()["pagination"]
    assert "items_per_page" in response.json()["pagination"]

def test_get_study_sessions_with_pagination():
    response = client.get("/api/study_sessions?page=1&page_size=5")
    assert response.status_code == 200
    assert "study_sessions" in response.json()
    assert response.json()["pagination"]["current_page"] == 1
    assert response.json()["pagination"]["items_per_page"] == 5

def test_get_study_session():
    response = client.get("/api/study_sessions/1")
    assert response.status_code == 200
    session = response.json()
    assert "id" in session
    assert "activity_name" in session
    assert "group_name" in session
    assert "start_time" in session
    assert "end_time" in session
    assert "review_items_count" in session

def test_get_study_session_not_found():
    response = client.get("/api/study_sessions/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session not found"

def test_get_session_words():
    response = client.get("/api/study_sessions/1/words")
    assert response.status_code == 200
    assert "words" in response.json()
    assert "pagination" in response.json()
    words = response.json()["words"]
    if len(words) > 0:
        word = words[0]
        assert "id" in word
        assert "jamaican_patois" in word
        assert "english" in word
        assert "parts" in word
        assert "correct_count" in word
        assert "wrong_count" in word

def test_get_session_words_with_pagination():
    response = client.get("/api/study_sessions/1/words?page=1&page_size=5")
    assert response.status_code == 200
    assert "words" in response.json()
    assert response.json()["pagination"]["current_page"] == 1
    assert response.json()["pagination"]["items_per_page"] == 5

def test_get_session_words_session_not_found():
    response = client.get("/api/study_sessions/9999/words")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session not found"

def test_create_word_review():
    response = client.post(
        "/api/study_sessions/1/words/1/review",
        json={"correct": True}
    )
    assert response.status_code == 200
    review = response.json()
    assert "id" in review
    assert "word_id" in review
    assert review["word_id"] == 1
    assert "study_session_id" in review
    assert review["study_session_id"] == 1
    assert "correct" in review
    assert review["correct"] is True
    assert "created_at" in review
    assert "word_jamaican_patois" in review
    assert "word_english" in review

def test_create_word_review_session_not_found():
    response = client.post(
        "/api/study_sessions/9999/words/1/review",
        json={"correct": True}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Study session not found"

def test_create_word_review_word_not_found():
    response = client.post(
        "/api/study_sessions/1/words/9999/review",
        json={"correct": True}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"

def test_create_word_review_word_not_in_session():
    # Assuming word ID 2 is not part of session 1
    response = client.post(
        "/api/study_sessions/1/words/2/review",
        json={"correct": True}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Word is not part of this study session" 