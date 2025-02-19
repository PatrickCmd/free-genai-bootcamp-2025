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

def test_get_study_activity():
    response = client.get("/api/study_activities/1")
    assert response.status_code == 200
    activity = response.json()
    assert "id" in activity
    assert "name" in activity
    assert "study_session_id" in activity
    assert "group_id" in activity
    assert "created_at" in activity
    assert "group_name" in activity
    assert "review_items_count" in activity

def test_get_study_activity_not_found():
    response = client.get("/api/study_activities/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study activity not found"

def test_get_activity_study_sessions():
    response = client.get("/api/study_activities/1/study_sessions")
    assert response.status_code == 200
    assert "study_sessions" in response.json()
    assert "pagination" in response.json()
    assert "current_page" in response.json()["pagination"]
    assert "total_pages" in response.json()["pagination"]
    assert "total_items" in response.json()["pagination"]
    assert "items_per_page" in response.json()["pagination"]

def test_get_activity_study_sessions_with_pagination():
    response = client.get("/api/study_activities/1/study_sessions?page=1&page_size=5")
    assert response.status_code == 200
    assert "study_sessions" in response.json()
    assert response.json()["pagination"]["current_page"] == 1
    assert response.json()["pagination"]["items_per_page"] == 5

def test_get_activity_study_sessions_not_found():
    response = client.get("/api/study_activities/9999/study_sessions")
    assert response.status_code == 404
    assert response.json()["detail"] == "Study activity not found"

def test_create_study_activity():
    response = client.post(
        "/api/study_activities",
        json={"name": "New Vocabulary Review", "group_id": 1}
    )
    assert response.status_code == 200
    activity = response.json()
    assert "id" in activity
    assert "name" in activity
    assert activity["name"] == "New Vocabulary Review"
    assert "study_session_id" in activity
    assert "group_id" in activity
    assert activity["group_id"] == 1
    assert "created_at" in activity
    assert "group_name" in activity
    assert "review_items_count" in activity

def test_create_study_activity_invalid_group():
    response = client.post(
        "/api/study_activities",
        json={"name": "New Vocabulary Review", "group_id": 9999}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found" 