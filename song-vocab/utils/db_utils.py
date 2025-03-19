import os
from pathlib import Path
from database import DatabaseStore, init_db

def get_db_store() -> DatabaseStore:
    """Get a configured database store instance"""
    db_path = os.getenv('DB_PATH', 'data/vocab.db')
    
    # Ensure database exists
    if not Path(db_path).exists():
        init_db(db_path)
    
    return DatabaseStore(db_path) 