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

def test_get_groups():
    response = client.get("/api/groups")
    assert response.status_code == 200
    assert "groups" in response.json()
    assert "pagination" in response.json()
    assert "current_page" in response.json()["pagination"]
    assert "total_pages" in response.json()["pagination"]
    assert "total_items" in response.json()["pagination"]
    assert "items_per_page" in response.json()["pagination"]

def test_get_groups_with_pagination():
    response = client.get("/api/groups?page=2&page_size=5")
    assert response.status_code == 200
    assert "groups" in response.json()
    assert response.json()["pagination"]["current_page"] == 2
    assert response.json()["pagination"]["items_per_page"] == 5

def test_get_group():
    response = client.get("/api/groups/1")
    assert response.status_code == 200
    group = response.json()
    assert "id" in group
    assert "name" in group
    assert "word_count" in group

def test_get_group_not_found():
    response = client.get("/api/groups/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found" 