import sys
import os
import pytest
from fastapi.testclient import TestClient
from lib.db import get_db_connection

# Add the backend directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.append(backend_dir)

from app import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_settings():
    """Reset settings to default before each test"""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM user_settings")
        conn.execute("""
            INSERT INTO user_settings (
                id, words_per_session, review_interval,
                show_phonetics, show_usage_examples, dark_mode
            ) VALUES (
                1, 10, 24, 1, 1, 1
            )
        """)

def test_get_settings_default():
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert data["wordsPerSession"] == 10
    assert data["reviewInterval"] == 24
    assert data["showPhonetics"] is True
    assert data["showUsageExamples"] is True
    assert data["darkMode"] is True

def test_update_settings():
    new_settings = {
        "wordsPerSession": 20,
        "reviewInterval": 48,
        "showPhonetics": False,
        "showUsageExamples": True,
        "darkMode": False
    }
    response = client.post("/api/settings", json=new_settings)
    assert response.status_code == 200
    data = response.json()
    assert data == new_settings

    # Verify settings were saved
    response = client.get("/api/settings")
    assert response.status_code == 200
    data = response.json()
    assert data == new_settings

def test_update_settings_validation():
    invalid_settings = {
        "wordsPerSession": -1,  # Invalid value
        "reviewInterval": 48,
        "showPhonetics": False,
        "showUsageExamples": True,
        "darkMode": False
    }
    response = client.post("/api/settings", json=invalid_settings)
    assert response.status_code == 422  # Validation error 