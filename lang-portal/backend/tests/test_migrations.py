import sys
import os
import pytest

# Add the backend directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.append(backend_dir)

from migrate import apply_migrations, rollback_migration
from lib.db import get_db_connection

@pytest.fixture
def in_memory_db():
    # Use an in-memory database for testing
    db_name = ":memory:"
    yield db_name

def test_apply_migrations(in_memory_db):
    # Test applying all migrations to an in-memory DB
    apply_migrations(in_memory_db)
    with get_db_connection(in_memory_db) as conn:
        # Check if a known table exists, for example:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
        assert cursor.fetchone() is not None, "Table 'words' should exist after migrations."

def test_rollback_migration(in_memory_db):
    # Apply migrations first
    apply_migrations(in_memory_db)
    # Rollback the last migration
    rollback_migration(in_memory_db)
    with get_db_connection(in_memory_db) as conn:
        # Check if the last migration was rolled back
        cursor = conn.execute("SELECT migration_name FROM schema_migrations ORDER BY id DESC LIMIT 1")
        last_migration = cursor.fetchone()
        assert last_migration is None, "Last migration should be rolled back." 