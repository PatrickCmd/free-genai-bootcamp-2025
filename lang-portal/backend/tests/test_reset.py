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

# Set environment variable for testing
os.environ["ENABLE_RESET"] = "true"

def test_reset_all_data():
    response = client.post("/api/reset/all")
    assert response.status_code == 200
    assert response.json()["message"] == "All data has been reset"
    
    # Verify data is reset
    groups = client.get("/api/groups")
    assert groups.json()["groups"] == []

def test_reset_study_data():
    # First seed some data
    client.post("/api/reset/seed")
    
    # Then reset study data
    response = client.post("/api/reset/study-data")
    assert response.status_code == 200
    assert response.json()["message"] == "Study data has been reset"
    
    # Verify study data is reset but words/groups remain
    study_sessions = client.get("/api/study_sessions")
    assert study_sessions.json()["study_sessions"] == []
    
    groups = client.get("/api/groups")
    assert len(groups.json()["groups"]) > 0

def test_seed_test_data():
    # First reset all data
    client.post("/api/reset/all")
    
    # Then seed test data
    response = client.post("/api/reset/seed")
    assert response.status_code == 200
    assert response.json()["message"] == "Test data has been seeded"
    
    # Verify test data is seeded
    groups = client.get("/api/groups")
    assert len(groups.json()["groups"]) > 0
    
    study_sessions = client.get("/api/study_sessions")
    assert len(study_sessions.json()["study_sessions"]) > 0 