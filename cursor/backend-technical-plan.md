Below is a high-level step-by-step plan that a junior developer could follow to implement the requirements using **FastAPI** (Python) and **SQLite3**, _without_ using ORM libraries like SQLAlchemy or Alembic. The plan focuses on:

1. Initializing the SQLite3 database with FastAPI, using raw SQL (no SQLAlchemy)  
2. Writing raw SQL scripts to create the database tables as specified  
3. Managing migrations (both forward and backward) manually using SQL scripts  
4. Developing the endpoints described in the spec  
5. Writing automated unit tests for these endpoints  

---

## 1. Initialize the SQLite3 Database with FastAPI

### 1.1 Create a Virtual Environment and Install Dependencies

1. Create and activate a virtual environment. For example:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install FastAPI and Uvicorn (for local development server):
   ```bash
   pip install fastapi uvicorn
   ```
3. Add other needed libraries (e.g., `pytest` for testing, `requests` for integration tests, etc.) to your `requirements.txt`:
   ```txt
   fastapi
   uvicorn
   pytest
   requests
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

### 1.2 Project Structure

Following the structure in the spec (slightly adjusted to match FastAPI conventions), you might end up with something like:

```
backend
├── Readme.md
├── requirements.txt
├── app.py                # FastAPI main entry
├── lib
│   └── db.py             # Database connection and utility functions
├── migrate.py            # Script to handle migrations
├── routes
│   ├── dashboard.py      # Endpoints for dashboard
│   ├── groups.py         # Endpoints for groups
│   ├── study_activities.py
│   ├── study_sessions.py
│   └── words.py
├── seed
│   ├── data_adjectives.json
│   ├── data_verbs.json
│   └── study_activities.json
├── sql
│   └── setup
│       ├── create_table_groups.sql
│       ├── create_table_study_activities.sql
│       ├── create_table_study_sessions.sql
│       ├── create_table_word_groups.sql
│       ├── create_table_word_review_items.sql
│       ├── create_table_word_reviews.sql
│       ├── create_table_words.sql
│       ├── create_word_reviews.sql
│       └── insert_study_activities.sql
└── tests                 # test folder
    ├── test_dashboard.py
    ├── test_groups.py
    ├── test_study_activities.py
    ├── test_study_sessions.py
    └── test_words.py
```

### 1.3 Setting Up the SQLite DB Connection

In `lib/db.py`, implement a simple function to get a database connection:

```python
import sqlite3
from contextlib import contextmanager

DB_NAME = "words.db"

@contextmanager
def get_db_connection():
    """Provide a transactional scope around a series of operations."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

This helper will allow you to do something like:

```python
from lib.db import get_db_connection

with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
```

This ensures each block either commits on success or rolls back on failure.

---

## 2. Write Raw SQL Scripts to Create All Database Tables

The spec outlines the tables required:

- `words`
- `word_groups`
- `groups`
- `study_sessions`
- `study_activities`
- `word_review_items`
- `word_reviews` (if needed)

Each `.sql` file in your `sql/setup/` folder might look like this:

### Example: `create_table_words.sql`
```sql
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jamaican_patois TEXT NOT NULL,
    english TEXT NOT NULL,
    parts JSON
);
```

### Example: `create_table_groups.sql`
```sql
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
```

…and so on for each table. You can refer back to the spec for the exact fields.

---

## 3. Write Migration Scripts (Manual, No Alembic)

Because we are _not_ using Alembic or any ORM, you will manage your migrations manually. The typical process is:

1. **Create a migrations folder** (e.g., `migrations/`) where you place SQL files like `0001_init.sql`, `0002_add_new_field.sql`, etc.
2. **Write an `UP` migration** in each file for the changes you want to apply (creating a table, adding columns, etc.).
3. **Optionally** keep a `DOWN` part in the same file if you want to be able to revert (roll back) that migration (dropping the table/columns, etc.).  

### 3.1 Tracking Applied Migrations

When not using a migration framework, a common approach is:

1. Create a table called `schema_migrations` in your DB:
   ```sql
   CREATE TABLE IF NOT EXISTS schema_migrations (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       migration_name TEXT NOT NULL,
       applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
2. Each time you run a new migration, you insert a record indicating that migration was applied.

### 3.2 A Simple `migrate.py` Script

In `migrate.py`, you might do something like:

```python
import os
from lib.db import get_db_connection

MIGRATIONS_DIR = "migrations"

def get_applied_migrations():
    """Return a set of applied migration filenames."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor = conn.execute("SELECT migration_name FROM schema_migrations")
        rows = cursor.fetchall()
    return set(row[0] for row in rows)

def migrate_up():
    """Apply all new migrations in ascending order."""
    applied = get_applied_migrations()
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

    for file in files:
        if file not in applied:
            path = os.path.join(MIGRATIONS_DIR, file)
            with open(path, "r") as f:
                sql_script = f.read()
            with get_db_connection() as conn:
                conn.executescript(sql_script)
                conn.execute("INSERT INTO schema_migrations (migration_name) VALUES (?)", (file,))
            print(f"Applied {file}")

def rollback_migration(migration_file):
    """Rollback a single migration if a 'DOWN' section is included."""
    # you'd parse the .sql file to separate the DOWN steps, or keep separate .down.sql files
    # then you'd execute them in reverse order to revert changes
    pass

if __name__ == "__main__":
    migrate_up()
```

For example, your `migrations/0001_init.sql` might contain multiple `CREATE TABLE` statements that set up your DB schema (mirroring what you have in `sql/setup/` if you want to unify them).  

**Note**: Some teams keep a separate concept of “setup scripts” for initial tables vs. actual “migration scripts.” You can decide how to separate them. The key idea is a record of which scripts have been applied so that repeated runs don’t attempt to reapply the same scripts.

---

## 4. Develop All Stated Endpoints

Below is an outline of how you might organize each endpoint in separate route files under `routes/`. In FastAPI, you’ll create “routers” that can then be included in your main `app.py`.

### 4.1 `app.py`

```python
from fastapi import FastAPI
from routes.dashboard import router as dashboard_router
from routes.groups import router as groups_router
from routes.study_activities import router as study_activities_router
from routes.study_sessions import router as study_sessions_router
from routes.words import router as words_router

app = FastAPI()

# Include the routers
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(groups_router, prefix="/api/groups", tags=["groups"])
app.include_router(study_activities_router, prefix="/api/study_activities", tags=["study_activities"])
app.include_router(study_sessions_router, prefix="/api/study_sessions", tags=["study_sessions"])
app.include_router(words_router, prefix="/api/words", tags=["words"])

# If needed, you can define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello from the language learning portal"}
```

#### 4.1.1 Running the app
```bash
uvicorn app:app --reload
```
Or define in a `tasks.py` script if you prefer.

---

### 4.2 Example: `routes/dashboard.py`

```python
from fastapi import APIRouter
from lib.db import get_db_connection
from datetime import datetime

router = APIRouter()

@router.get("/last_study_session")
def get_last_study_session():
    """
    Returns information about the most recent study session.
    Example JSON Response:
    {
      "id": 123,
      "group_id": 456,
      "created_at": "2025-02-08T17:20:23-05:00",
      "study_activity_id": 789,
      "group_name": "Basic Greetings"
    }
    """
    with get_db_connection() as conn:
        cursor = conn.execute("""
            SELECT ss.id, ss.group_id, ss.created_at, ss.study_activity_id,
                   g.name as group_name
            FROM study_sessions ss
            LEFT JOIN groups g on ss.group_id = g.id
            ORDER BY ss.created_at DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
    
    if row:
        return {
            "id": row[0],
            "group_id": row[1],
            "created_at": row[2],
            "study_activity_id": row[3],
            "group_name": row[4]
        }
    else:
        return {}  # or a 404 Not Found

@router.get("/study_progress")
def get_study_progress():
    """
    Returns study progress statistics.
    Example JSON Response:
    {
      "total_words_studied": 3,
      "total_available_words": 124
    }
    """
    # total_words_studied = count unique words in word_review_items that have correct or wrong reviews
    # total_available_words = count of words in 'words' table
    with get_db_connection() as conn:
        cursor1 = conn.execute("SELECT COUNT(DISTINCT word_id) FROM word_review_items")
        total_words_studied = cursor1.fetchone()[0]

        cursor2 = conn.execute("SELECT COUNT(*) FROM words")
        total_available_words = cursor2.fetchone()[0]

    return {
        "total_words_studied": total_words_studied,
        "total_available_words": total_available_words
    }

@router.get("/quick-stats")
def get_quick_stats():
    """
    Returns quick overview stats:
    {
      "success_rate": 80.0,
      "total_study_sessions": 4,
      "total_active_groups": 3,
      "study_streak_days": 4
    }
    """
    with get_db_connection() as conn:
        # success_rate could be ratio of correct reviews vs total reviews
        cursor = conn.execute("""
            SELECT
                (SELECT COUNT(*) FROM word_review_items WHERE correct=1) * 1.0 /
                (SELECT COUNT(*) FROM word_review_items) * 100.0 as success_rate,
                (SELECT COUNT(*) FROM study_sessions) as total_study_sessions,
                (SELECT COUNT(*) FROM groups) as total_active_groups
        """)
        row = cursor.fetchone()
        success_rate = row[0] if row and row[0] is not None else 0
        total_study_sessions = row[1] if row else 0
        total_active_groups = row[2] if row else 0

    # For a real "streak," you'd track daily usage. We'll just mock it here:
    study_streak_days = 4

    return {
        "success_rate": float(success_rate),
        "total_study_sessions": total_study_sessions,
        "total_active_groups": total_active_groups,
        "study_streak_days": study_streak_days
    }
```

### 4.3 Other Endpoints

You would create similar router files for:

- **Words** (`routes/words.py`)
- **Groups** (`routes/groups.py`)
- **Study Activities** (`routes/study_activities.py`)
- **Study Sessions** (`routes/study_sessions.py`)

And implement each route from the specification:

- **GET /api/words**, **GET /api/words/:id**, etc.
- **GET /api/groups**, **GET /api/groups/:id**, etc.
- **GET /api/study_activities/:id**, **POST /api/study_activities**, etc.
- **GET /api/study_sessions**, **POST /api/study_sessions/:id/words/:word_id/review**, etc.
- **POST /api/reset_history**, **POST /api/full_reset**, etc.

Remember to handle:
1. **Pagination** (by adding `limit` and `offset` or `page` query parameters)
2. **JSON responses** (FastAPI returns JSON by default)
3. **No authentication** (simplifies your code)
4. **Single user** scenario

---

## 5. Write Automated Unit Tests

### 5.1 Testing Strategy

A simple approach is to use [Pytest](https://docs.pytest.org/) with [FastAPI’s TestClient](https://fastapi.tiangolo.com/tutorial/testing/).  

1. Create a `tests/` folder.
2. In each test file, import the FastAPI `app` and the `TestClient`.
3. Use the client to call your endpoints and assert the results.

### 5.2 Example: `tests/test_dashboard.py`

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_last_study_session_empty():
    """
    If the DB is empty or no study sessions, expect an empty dict or 404 response.
    """
    response = client.get("/api/dashboard/last_study_session")
    assert response.status_code == 200
    data = response.json()
    # Depending on how you handle empty, might be {}
    # If you do "return {}" instead of 404
    assert data == {}

def test_get_study_progress():
    """
    Assuming you have seeded data or pre-inserted data for the test DB.
    Check if the stats come back as expected.
    """
    # You might seed the DB in a setup step, then call
    response = client.get("/api/dashboard/study_progress")
    assert response.status_code == 200
    data = response.json()
    assert "total_words_studied" in data
    assert "total_available_words" in data
```

### 5.3 Running Tests

```bash
pytest tests/
```

Or specify a coverage report:

```bash
pytest --cov=.
```

---

# Putting It All Together

1. **Create and activate a virtual environment**; install necessary packages.  
2. **Write your raw SQL table creation scripts** in `sql/setup/`.  
3. **Write your manual migrations** in `migrations/`.  
4. **Implement the `migrate.py` script** to run those migrations on `words.db`.  
5. **Create `app.py`** for FastAPI and your `routes/` modules.  
6. **Build each endpoint** carefully, referencing the specification for JSON responses and route signatures.  
7. **Create unit tests** in `tests/` using `pytest` and `TestClient`.  
8. **Run your tests** to verify each endpoint’s behavior.  

At the end of this process, you’ll have:

- A **FastAPI** application with the specified endpoints  
- A **SQLite** database with the necessary tables  
- A **Manual migration** system to handle schema updates  
- A **Set of automated tests** to verify your endpoints  

Following these steps will satisfy the given requirements and produce a clean, maintainable prototype for the language-learning school system.