```markdown
# Plan for Implementing All API Endpoints

This plan outlines the steps for a junior developer to implement all the API endpoints in their respective modules using **FastAPI** with raw SQLite (no ORM). Each section corresponds to a single `routes/*.py` module. The plan also includes simple testing snippets that can be placed in `tests/*.py`.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Dashboard Endpoints (`routes/dashboard.py`)](#dashboard-endpoints-routesdashboardpy)
3. [Words Endpoints (`routes/words.py`)](#words-endpoints-routeswordspy)
4. [Groups Endpoints (`routes/groups.py`)](#groups-endpoints-routesgroupspy)
5. [Study Activities Endpoints (`routes/study_activities.py`)](#study-activities-endpoints-routesstudy_activitiespy)
6. [Study Sessions Endpoints (`routes/study_sessions.py`)](#study-sessions-endpoints-routesstudy_sessionspy)
7. [Reset Endpoints (in a suitable file, e.g., `routes/reset.py`)](#reset-endpoints-in-a-suitable-file-eg-routesresetpy)
8. [General Testing Tips](#general-testing-tips)

---

## Prerequisites

- [ ] **Create** or **Verify** that you have a `lib/db.py` with a `get_db_connection()` function returning a raw SQLite connection.
- [ ] **Confirm** that `app.py` (your main FastAPI file) includes router imports, e.g.:

  ```python
  from fastapi import FastAPI
  from routes.dashboard import router as dashboard_router
  from routes.words import router as words_router
  from routes.groups import router as groups_router
  from routes.study_activities import router as study_activities_router
  from routes.study_sessions import router as study_sessions_router
  from routes.reset import router as reset_router  # if you put reset endpoints here

  app = FastAPI()

  app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
  app.include_router(words_router, prefix="/api/words", tags=["words"])
  app.include_router(groups_router, prefix="/api/groups", tags=["groups"])
  app.include_router(study_activities_router, prefix="/api/study_activities", tags=["study_activities"])
  app.include_router(study_sessions_router, prefix="/api/study_sessions", tags=["study_sessions"])
  app.include_router(reset_router, prefix="/api", tags=["reset"])
  ```
- [ ] **Ensure** you have your database set up (via `migrate.py` or raw scripts).  

---

## Dashboard Endpoints (`routes/dashboard.py`)

**Endpoints:**
1. `GET /api/dashboard/last_study_session`
2. `GET /api/dashboard/study_progress`
3. `GET /api/dashboard/quick-stats`

### Steps

1. [x] **Create** a file: `routes/dashboard.py`.
2. [x] **Import** necessary modules:
   ```python
   from fastapi import APIRouter
   from lib.db import get_db_connection

   router = APIRouter()
   ```
3. [x] **Implement** `GET /api/dashboard/last_study_session`:
   ```python
   @router.get("/last_study_session")
   def get_last_study_session():
       with get_db_connection() as conn:
           cursor = conn.execute("""
               SELECT ss.id, ss.group_id, ss.created_at, ss.study_activity_id, g.name AS group_name
               FROM study_sessions ss
               LEFT JOIN groups g ON ss.group_id = g.id
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
       return {}
   ```
4. [x] **Implement** `GET /api/dashboard/study_progress`:
   ```python
   @router.get("/study_progress")
   def get_study_progress():
       with get_db_connection() as conn:
           # total words studied
           cursor = conn.execute("SELECT COUNT(DISTINCT word_id) FROM word_review_items")
           total_words_studied = cursor.fetchone()[0] or 0

           # total available words
           cursor = conn.execute("SELECT COUNT(*) FROM words")
           total_available_words = cursor.fetchone()[0] or 0

       return {
           "total_words_studied": total_words_studied,
           "total_available_words": total_available_words
       }
   ```
5. [x] **Implement** `GET /api/dashboard/quick-stats`:
   ```python
   @router.get("/quick-stats")
   def get_quick_stats():
       with get_db_connection() as conn:
           cursor = conn.execute("""
               SELECT
                 (SELECT COUNT(*) FROM word_review_items WHERE correct = 1) * 1.0 /
                 (SELECT COUNT(*) FROM word_review_items) * 100.0 AS success_rate,
                 (SELECT COUNT(*) FROM study_sessions) AS total_study_sessions,
                 (SELECT COUNT(*) FROM groups) AS total_active_groups
           """)
           row = cursor.fetchone()

       success_rate = row[0] if row and row[0] is not None else 0
       total_study_sessions = row[1] or 0
       total_active_groups = row[2] or 0
       # For demonstration, assume a static 4-day streak
       study_streak_days = 4

       return {
           "success_rate": float(success_rate),
           "total_study_sessions": total_study_sessions,
           "total_active_groups": total_active_groups,
           "study_streak_days": study_streak_days
       }
   ```

### Testing Snippet

Create a file `tests/test_dashboard.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_last_study_session():
    response = client.get("/api/dashboard/last_study_session")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_study_progress():
    response = client.get("/api/dashboard/study_progress")
    assert response.status_code == 200
    data = response.json()
    assert "total_words_studied" in data
    assert "total_available_words" in data

def test_get_quick_stats():
    response = client.get("/api/dashboard/quick-stats")
    assert response.status_code == 200
    data = response.json()
    assert "success_rate" in data
    assert "total_study_sessions" in data
    assert "total_active_groups" in data
    assert "study_streak_days" in data
```

---

## Words Endpoints (`routes/words.py`)

**Endpoints:**
1. `GET /api/words` (with pagination)
2. `GET /api/words/{id}`
3. Potential additional routes in the future

### Steps

1. [x] **Create** `routes/words.py`.
2. [x] **Import** modules:
   ```python
   from fastapi import APIRouter, Query
   from lib.db import get_db_connection

   router = APIRouter()
   ```
3. [x] **Implement** `GET /api/words`:
   - **Goal**: Return paginated list of words with stats (correct/wrong counts).
   - For demonstration, assume 100 items per page.  
   ```python
   @router.get("/")
   def list_words(page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           # 1) get total count
           cursor_count = conn.execute("SELECT COUNT(*) FROM words")
           total_items = cursor_count.fetchone()[0]

           # 2) fetch words
           cursor_words = conn.execute("""
               SELECT w.id, w.jamaican_patois, w.english,
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = w.id AND correct = 1) AS correct_count,
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = w.id AND correct = 0) AS wrong_count
               FROM words w
               LIMIT ? OFFSET ?
           """, (limit, offset))

           rows = cursor_words.fetchall()

       items = []
       for row in rows:
           items.append({
               "id": row[0],
               "jamaican patois": row[1],
               "english": row[2],
               "correct_count": row[3],
               "wrong_count": row[4]
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
4. [ ] **Implement** `GET /api/words/{word_id}`:
   ```python
   @router.get("/{word_id}")
   def get_word(word_id: int):
       with get_db_connection() as conn:
           # fetch word
           cursor_word = conn.execute("""
               SELECT w.id, w.jamaican_patois, w.english
               FROM words w
               WHERE w.id = ?
           """, (word_id,))
           row = cursor_word.fetchone()

           if not row:
               return {}  # or raise HTTPException(status_code=404, detail="Word not found")

           # fetch stats
           cursor_stats = conn.execute("""
               SELECT
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = ? AND correct = 1) AS correct_count,
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = ? AND correct = 0) AS wrong_count
           """, (word_id, word_id))
           stats_row = cursor_stats.fetchone()

           # fetch groups
           cursor_groups = conn.execute("""
               SELECT g.id, g.name
               FROM groups g
               JOIN word_groups wg ON g.id = wg.group_id
               WHERE wg.word_id = ?
           """, (word_id,))
           groups_rows = cursor_groups.fetchall()

       groups_list = [{"id": g[0], "name": g[1]} for g in groups_rows]

       return {
           "id": row[0],
           "jamaican patois": row[1],
           "english": row[2],
           "stats": {
               "correct_count": stats_row[0],
               "wrong_count": stats_row[1]
           },
           "groups": groups_list
       }
   ```

### Testing Snippet

Create `tests/test_words.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_list_words():
    response = client.get("/api/words?page=1")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "pagination" in data

def test_get_word():
    # This test assumes a word with id=1 exists in the database.
    response = client.get("/api/words/1")
    assert response.status_code == 200
    data = response.json()
    if data:  # if the word exists
        assert "jamaican patois" in data
        assert "english" in data
        assert "stats" in data
        assert "groups" in data
```

---

## Groups Endpoints (`routes/groups.py`)

**Endpoints:**
1. `GET /api/groups` (with pagination)
2. `GET /api/groups/{id}`
3. `GET /api/groups/{id}/words`
4. `GET /api/groups/{id}/study_sessions`

### Steps

1. [x] **Create** `routes/groups.py`.
2. [x] **Import** modules:
   ```python
   from fastapi import APIRouter, Query
   from lib.db import get_db_connection

   router = APIRouter()
   ```
3. [x] **Implement** `GET /api/groups`:
   ```python
   @router.get("/")
   def list_groups(page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           cursor_count = conn.execute("SELECT COUNT(*) FROM groups")
           total_items = cursor_count.fetchone()[0]

           cursor_groups = conn.execute("""
               SELECT g.id, g.name,
                 (SELECT COUNT(*) FROM word_groups wg WHERE wg.group_id = g.id) as word_count
               FROM groups g
               LIMIT ? OFFSET ?
           """, (limit, offset))

           rows = cursor_groups.fetchall()

       items = []
       for row in rows:
           items.append({
               "id": row[0],
               "name": row[1],
               "word_count": row[2],
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
4. [x] **Implement** `GET /api/groups/{group_id}`:
   ```python
   @router.get("/{group_id}")
   def get_group(group_id: int):
       with get_db_connection() as conn:
           cursor = conn.execute("""
               SELECT g.id, g.name
               FROM groups g
               WHERE g.id = ?
           """, (group_id,))
           row = cursor.fetchone()
           if not row:
               return {}  # or raise HTTPException(status_code=404, detail="Group not found")

           cursor_count = conn.execute("""
               SELECT COUNT(*)
               FROM word_groups
               WHERE group_id = ?
           """, (group_id,))
           total_word_count = cursor_count.fetchone()[0]

       return {
           "id": row[0],
           "name": row[1],
           "stats": {
               "total_word_count": total_word_count
           }
       }
   ```
5. [x] **Implement** `GET /api/groups/{group_id}/words`:
   ```python
   @router.get("/{group_id}/words")
   def get_group_words(group_id: int, page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           # count total items
           cursor_count = conn.execute("""
               SELECT COUNT(*) 
               FROM word_groups wg
               WHERE wg.group_id = ?
           """, (group_id,))
           total_items = cursor_count.fetchone()[0]

           cursor_words = conn.execute("""
               SELECT w.id, w.jamaican_patois, w.english,
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = w.id AND correct = 1) AS correct_count,
                 (SELECT COUNT(*) FROM word_review_items WHERE word_id = w.id AND correct = 0) AS wrong_count
               FROM word_groups wg
               JOIN words w ON wg.word_id = w.id
               WHERE wg.group_id = ?
               LIMIT ? OFFSET ?
           """, (group_id, limit, offset))
           rows = cursor_words.fetchall()

       items = []
       for row in rows:
           items.append({
               "jamaican patois": row[1],
               "english": row[2],
               "correct_count": row[3],
               "wrong_count": row[4],
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
6. [x] **Implement** `GET /api/groups/{group_id}/study_sessions`:
   ```python
   @router.get("/{group_id}/study_sessions")
   def get_group_study_sessions(group_id: int, page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           # Count total
           cursor_count = conn.execute("""
               SELECT COUNT(*)
               FROM study_sessions
               WHERE group_id = ?
           """, (group_id,))
           total_items = cursor_count.fetchone()[0]

           cursor_sessions = conn.execute("""
               SELECT ss.id,
                      (SELECT name FROM study_activities sa WHERE sa.id = ss.study_activity_id) AS activity_name,
                      (SELECT name FROM groups g WHERE g.id = ss.group_id) AS group_name,
                      ss.created_at AS start_time,
                      NULL AS end_time,  -- or if you store an end_time, select it
                      (SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) as review_items_count
               FROM study_sessions ss
               WHERE ss.group_id = ?
               LIMIT ? OFFSET ?
           """, (group_id, limit, offset))

           rows = cursor_sessions.fetchall()

       items = []
       for row in rows:
           items.append({
               "id": row[0],
               "activity_name": row[1],
               "group_name": row[2],
               "start_time": row[3],
               "end_time": row[4],
               "review_items_count": row[5]
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```

### Testing Snippet

Create `tests/test_groups.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_list_groups():
    response = client.get("/api/groups")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "pagination" in data

def test_get_group():
    response = client.get("/api/groups/1")  # adjust ID as needed
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "id" in data
        assert "name" in data
        assert "stats" in data

def test_get_group_words():
    response = client.get("/api/groups/1/words")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_get_group_study_sessions():
    response = client.get("/api/groups/1/study_sessions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
```

---

## Study Activities Endpoints (`routes/study_activities.py`)

**Endpoints:**
1. `GET /api/study_activities/{id}`
2. `GET /api/study_activities/{id}/study_sessions`
3. `POST /api/study_activities` (start a study session)

### Steps

1. [x] **Create** `routes/study_activities.py`.
2. [x] **Import** modules:
   ```python
   from fastapi import APIRouter, Query, Body
   from lib.db import get_db_connection
   from pydantic import BaseModel

   router = APIRouter()
   ```
3. [x] **Implement** `GET /api/study_activities/{id}`:
   ```python
   @router.get("/{activity_id}")
   def get_study_activity(activity_id: int):
       with get_db_connection() as conn:
           cursor = conn.execute("""
               SELECT id, 'Vocabulary Quiz' as name, 'https://example.com/thumbnail.jpg' as thumbnail_url,
               'Practice your vocabulary with flashcards' as description
               FROM study_activities
               WHERE id = ?
           """, (activity_id,))
           row = cursor.fetchone()

       if not row:
           return {}  # or 404

       return {
           "id": row[0],
           "name": row[1],
           "thumbnail_url": row[2],
           "description": row[3]
       }
   ```
   *(Adjust query and columns to match your actual schema.)*

4. [x] **Implement** `GET /api/study_activities/{activity_id}/study_sessions`:
   ```python
   @router.get("/{activity_id}/study_sessions")
   def get_study_activity_sessions(activity_id: int, page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           # Count total
           cursor_count = conn.execute("""
               SELECT COUNT(*) 
               FROM study_sessions
               WHERE study_activity_id = ?
           """, (activity_id,))
           total_items = cursor_count.fetchone()[0]

           cursor_sessions = conn.execute("""
               SELECT ss.id,
                      (SELECT name FROM study_activities sa WHERE sa.id = ss.study_activity_id) AS activity_name,
                      (SELECT name FROM groups g WHERE g.id = ss.group_id) AS group_name,
                      ss.created_at AS start_time,
                      NULL AS end_time,
                      (SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) AS review_items_count
               FROM study_sessions ss
               WHERE ss.study_activity_id = ?
               LIMIT ? OFFSET ?
           """, (activity_id, limit, offset))
           rows = cursor_sessions.fetchall()

       items = []
       for row in rows:
           items.append({
               "id": row[0],
               "activity_name": row[1],
               "group_name": row[2],
               "start_time": row[3],
               "end_time": row[4],
               "review_items_count": row[5]
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
5. [x] **Implement** `POST /api/study_activities` (start session):
   - The request params: `group_id` and `study_activity_id`.
   - This may create a new `study_sessions` record.

   ```python
   from datetime import datetime

   class StartSessionRequest(BaseModel):
       group_id: int
       study_activity_id: int

   @router.post("/")
   def start_study_session(payload: StartSessionRequest):
       with get_db_connection() as conn:
           # Insert a new row in study_sessions
           now_str = datetime.utcnow().isoformat()
           cursor = conn.execute("""
               INSERT INTO study_sessions (group_id, created_at, study_activity_id)
               VALUES (?, ?, ?)
           """, (payload.group_id, now_str, payload.study_activity_id))
           session_id = cursor.lastrowid

       return {
           "id": session_id,
           "group_id": payload.group_id
       }
   ```

### Testing Snippet

Create `tests/test_study_activities.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_study_activity():
    response = client.get("/api/study_activities/1")
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "id" in data
        assert "name" in data
        assert "thumbnail_url" in data
        assert "description" in data

def test_get_study_activity_sessions():
    response = client.get("/api/study_activities/1/study_sessions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_post_study_activities():
    payload = {"group_id": 1, "study_activity_id": 1}
    response = client.post("/api/study_activities", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "group_id" in data
```

---

## Study Sessions Endpoints (`routes/study_sessions.py`)

**Endpoints:**
1. `GET /api/study_sessions` (paginated)
2. `GET /api/study_sessions/{id}`
3. `GET /api/study_sessions/{id}/words`
4. `POST /api/study_sessions/{id}/words/{word_id}/review`

### Steps

1. [x] **Create** `routes/study_sessions.py`.
2. [x] **Import** modules:
   ```python
   from fastapi import APIRouter, Query, Body, HTTPException
   from lib.db import get_db_connection
   from pydantic import BaseModel

   router = APIRouter()
   ```
3. [x] **Implement** `GET /api/study_sessions`:
   ```python
   @router.get("/")
   def list_study_sessions(page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           cursor_count = conn.execute("SELECT COUNT(*) FROM study_sessions")
           total_items = cursor_count.fetchone()[0]

           cursor_sessions = conn.execute("""
               SELECT ss.id,
                      (SELECT name FROM study_activities sa WHERE sa.id = ss.study_activity_id) AS activity_name,
                      (SELECT name FROM groups g WHERE g.id = ss.group_id) AS group_name,
                      ss.created_at AS start_time,
                      NULL AS end_time,
                      (SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) AS review_items_count
               FROM study_sessions ss
               LIMIT ? OFFSET ?
           """, (limit, offset))
           rows = cursor_sessions.fetchall()

       items = []
       for row in rows:
           items.append({
               "id": row[0],
               "activity_name": row[1],
               "group_name": row[2],
               "start_time": row[3],
               "end_time": row[4],
               "review_items_count": row[5]
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
4. [x] **Implement** `GET /api/study_sessions/{id}`:
   ```python
   @router.get("/{session_id}")
   def get_study_session(session_id: int):
       with get_db_connection() as conn:
           cursor = conn.execute("""
               SELECT ss.id,
                      (SELECT name FROM study_activities sa WHERE sa.id = ss.study_activity_id) AS activity_name,
                      (SELECT name FROM groups g WHERE g.id = ss.group_id) AS group_name,
                      ss.created_at AS start_time,
                      NULL AS end_time,
                      (SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) AS review_items_count
               FROM study_sessions ss
               WHERE ss.id = ?
           """, (session_id,))
           row = cursor.fetchone()

       if not row:
           return {}  # or raise HTTPException(status_code=404)

       return {
           "id": row[0],
           "activity_name": row[1],
           "group_name": row[2],
           "start_time": row[3],
           "end_time": row[4],
           "review_items_count": row[5]
       }
   ```
5. [x] **Implement** `GET /api/study_sessions/{session_id}/words`:
   ```python
   @router.get("/{session_id}/words")
   def get_study_session_words(session_id: int, page: int = Query(1, ge=1)):
       limit = 100
       offset = (page - 1) * limit

       with get_db_connection() as conn:
           # count how many words in the session (in word_review_items)
           cursor_count = conn.execute("""
               SELECT COUNT(DISTINCT word_id) 
               FROM word_review_items
               WHERE study_session_id = ?
           """, (session_id,))
           total_items = cursor_count.fetchone()[0]

           cursor_words = conn.execute("""
               SELECT w.id, w.jamaican_patois, w.english,
                 (SELECT COUNT(*) FROM word_review_items wri WHERE wri.word_id = w.id AND wri.correct = 1) AS correct_count,
                 (SELECT COUNT(*) FROM word_review_items wri WHERE wri.word_id = w.id AND wri.correct = 0) AS wrong_count
               FROM word_review_items wri
               JOIN words w ON wri.word_id = w.id
               WHERE wri.study_session_id = ?
               GROUP BY w.id
               LIMIT ? OFFSET ?
           """, (session_id, limit, offset))
           rows = cursor_words.fetchall()

       items = []
       for row in rows:
           items.append({
               "jamaican patois": row[1],
               "english": row[2],
               "correct_count": row[3],
               "wrong_count": row[4]
           })

       total_pages = (total_items + limit - 1) // limit if total_items else 1

       return {
           "items": items,
           "pagination": {
               "current_page": page,
               "total_pages": total_pages,
               "total_items": total_items,
               "items_per_page": limit
           }
       }
   ```
6. [x] **Implement** `POST /api/study_sessions/{session_id}/words/{word_id}/review`:
   - Request body: `{"correct": true/false}`
   - Insert a `word_review_items` record

   ```python
   class ReviewItem(BaseModel):
       correct: bool

   @router.post("/{session_id}/words/{word_id}/review")
   def review_word_in_session(session_id: int, word_id: int, review: ReviewItem):
       with get_db_connection() as conn:
           # Optionally verify the session or the word exist
           now_str = datetime.utcnow().isoformat()

           conn.execute("""
               INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
               VALUES (?, ?, ?, ?)
           """, (word_id, session_id, 1 if review.correct else 0, now_str))

       return {
           "success": True,
           "word_id": word_id,
           "study_session_id": session_id,
           "correct": review.correct,
           "created_at": now_str
       }
   ```

### Testing Snippet

Create `tests/test_study_sessions.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_list_study_sessions():
    response = client.get("/api/study_sessions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_get_study_session():
    response = client.get("/api/study_sessions/1")  # adjust ID if needed
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "id" in data

def test_get_study_session_words():
    response = client.get("/api/study_sessions/1/words")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_review_word_in_session():
    payload = {"correct": True}
    response = client.post("/api/study_sessions/1/words/1/review", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["correct"] == True
```

---

## Reset Endpoints (in a suitable file, e.g., `routes/reset.py`)

**Endpoints:**
1. `POST /api/reset_history`
2. `POST /api/full_reset`

### Steps

1. [ ] **Create** `routes/reset.py`.
2. [ ] **Import** modules:
   ```python
   from fastapi import APIRouter
   from lib.db import get_db_connection

   router = APIRouter()
   ```
3. [ ] **Implement** `POST /api/reset_history`:
   - Clear all records from `word_review_items`, `study_sessions` but **keep** the words and groups.

   ```python
   @router.post("/reset_history")
   def reset_history():
       with get_db_connection() as conn:
           conn.execute("DELETE FROM word_review_items")
           conn.execute("DELETE FROM study_sessions")
           # Possibly handle other references
       return {
           "success": True,
           "message": "Study history has been reset"
       }
   ```
4. [ ] **Implement** `POST /api/full_reset`:
   - **Drop** or **truncate** all tables and re-create them, or just remove the DB file. Then re-run the migrations. 
   - For a simpler approach: just delete from all the main tables (words, groups, word_groups, study_sessions, etc.).

   ```python
   @router.post("/full_reset")
   def full_reset():
       with get_db_connection() as conn:
           # remove data from all tables
           conn.execute("DELETE FROM word_review_items")
           conn.execute("DELETE FROM study_sessions")
           conn.execute("DELETE FROM words")
           conn.execute("DELETE FROM groups")
           conn.execute("DELETE FROM word_groups")
           # etc.

       return {
           "success": True,
           "message": "System has been fully reset"
       }
   ```

### Testing Snippet

Create `tests/test_reset.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_reset_history():
    response = client.post("/api/reset_history")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_full_reset():
    response = client.post("/api/full_reset")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

---

## General Testing Tips

- [ ] **Use** a dedicated test database or a temporary SQLite in-memory DB for tests.
- [ ] **Seed** some test data in a `pytest` fixture or setup function to have consistent data for your tests.
- [ ] **Check** that your endpoints return the structure and HTTP status codes you expect.
- [ ] **Run** your tests:
  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```

---

**That’s it!** Following the above atomic tasks (with checkboxes) will allow you to methodically implement and test all endpoints as specified. Good luck!