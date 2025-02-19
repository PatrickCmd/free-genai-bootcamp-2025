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

def test_get_last_study_session():
    response = client.get("/api/dashboard/last_study_session")
    assert response.status_code == 200
    session = response.json()
    assert "id" in session
    assert "activity_name" in session
    assert "group_name" in session
    assert "start_time" in session
    assert "end_time" in session
    assert "review_items_count" in session

def test_get_last_study_session_no_sessions():
    # This test might need to be adjusted based on how you want to handle the case
    # when there are no sessions in the test database
    response = client.get("/api/dashboard/last_study_session")
    if response.status_code == 404:
        assert response.json()["detail"] == "No study sessions found"
    else:
        assert response.status_code == 200 

def test_get_study_progress():
    response = client.get("/api/dashboard/study_progress")
    assert response.status_code == 200
    progress = response.json()
    
    # Check all required fields are present
    assert "total_words_reviewed" in progress
    assert "total_correct" in progress
    assert "total_incorrect" in progress
    assert "accuracy_rate" in progress
    assert "total_study_sessions" in progress
    assert "total_study_time_minutes" in progress
    assert "words_by_group" in progress
    
    # Validate data types and ranges
    assert isinstance(progress["total_words_reviewed"], int)
    assert isinstance(progress["total_correct"], int)
    assert isinstance(progress["total_incorrect"], int)
    assert isinstance(progress["accuracy_rate"], float)
    assert 0 <= progress["accuracy_rate"] <= 100
    assert isinstance(progress["total_study_sessions"], int)
    assert isinstance(progress["total_study_time_minutes"], int)
    assert isinstance(progress["words_by_group"], list)
    
    # Check group statistics if any exist
    if progress["words_by_group"]:
        group = progress["words_by_group"][0]
        assert "group_id" in group
        assert "group_name" in group
        assert "unique_words" in group
        assert "total_reviews" in group
        assert "correct_reviews" in group
        assert "accuracy_rate" in group
        assert 0 <= group["accuracy_rate"] <= 100 

def test_get_quick_stats():
    response = client.get("/api/dashboard/quick-stats")
    assert response.status_code == 200
    stats = response.json()
    
    # Check all required fields are present
    assert "total_words" in stats
    assert "words_learned" in stats
    assert "total_study_time_minutes" in stats
    assert "recent_accuracy" in stats
    assert "streak_days" in stats
    
    # Validate data types and ranges
    assert isinstance(stats["total_words"], int)
    assert isinstance(stats["words_learned"], int)
    assert isinstance(stats["total_study_time_minutes"], int)
    assert isinstance(stats["recent_accuracy"], float)
    assert 0 <= stats["recent_accuracy"] <= 100
    assert isinstance(stats["streak_days"], int)
    assert stats["streak_days"] >= 0
    
    # Validate logical constraints
    assert stats["words_learned"] <= stats["total_words"] 