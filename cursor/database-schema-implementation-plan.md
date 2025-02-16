```markdown
# Plan for Creating, Initializing, and Managing the Database

This plan focuses on **SQLite** with **raw SQL scripts**, plus **manual migration** management (no ORM or Alembic). We will:

1. Create the initial database file  
2. Write raw SQL scripts to create tables  
3. Implement a migration system that runs these scripts in a controlled fashion  

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Create & Initialize the SQLite Database](#create--initialize-the-sqlite-database)  
4. [Database Table Scripts](#database-table-scripts)  
5. [Manual Migrations (No Alembic)](#manual-migrations-no-alembic)  
6. [Automated Testing Considerations](#automated-testing-considerations)

---

## Prerequisites

- [ ] **Install Python 3.7+** and set up a virtual environment if desired:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] **Have SQLite** installed or readily available on your system (most systems come with it by default).
- [ ] **Understand** basic SQL commands: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, etc.

---

## Project Structure

Below is an example folder layout focusing on database initialization and migrations. Adjust as needed:

```
backend
├── Readme.md
├── app.py                # (Optional) Main application file (e.g. FastAPI or any other).
├── lib
│   └── db.py             # Database connection and utilities.
├── migrate.py            # Migration script to apply or rollback changes.
├── sql
│   ├── setup             # Folder containing initial SQL scripts for table creation
│   │   ├── create_table_groups.sql
│   │   ├── create_table_study_activities.sql
│   │   ├── create_table_study_sessions.sql
│   │   ├── create_table_word_groups.sql
│   │   ├── create_table_word_review_items.sql
│   │   ├── create_table_word_reviews.sql
│   │   └── create_table_words.sql
│   └── migrations        # Folder containing sequential migration files
│       ├── 0001_init.sql
│       ├── 0002_add_column_x.sql
│       └── ...
└── tests
    └── test_migrations.py
```

**Notes**:
- `sql/setup` holds the initial scripts you run to create the tables from scratch.  
- `sql/migrations` holds subsequent scripts for incremental changes to the schema (manual migrations).  
- `migrate.py` is our custom script to apply migrations in the correct order.  

---

## Create & Initialize the SQLite Database

### Steps

1. [ ] **Create** a file `lib/db.py` to manage the connection:
   ```python
   import sqlite3
   from contextlib import contextmanager
   import os

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

2. [ ] **Decide** on a location for the `words.db` file (project root vs. a dedicated folder).
3. [ ] **Verify** that your `.gitignore` excludes `words.db` if you don’t want it in version control.

4. [ ] (Optional) **Test** the connection:
   ```python
   # Quick test
   from lib.db import get_db_connection

   with get_db_connection() as conn:
       print("Opened database successfully!")
   ```

---

## Database Table Scripts

We’ll store the raw SQL in `sql/setup/`. Here’s an example set of scripts based on the specs:

1. [ ] **create_table_words.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS words (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       jamaican_patois TEXT NOT NULL,
       english TEXT NOT NULL,
       parts JSON
   );
   ```

2. [ ] **create_table_groups.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS groups (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL
   );
   ```

3. [ ] **create_table_word_groups.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS word_groups (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       word_id INTEGER NOT NULL,
       group_id INTEGER NOT NULL
   );
   ```

4. [ ] **create_table_study_sessions.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS study_sessions (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       group_id INTEGER NOT NULL,
       created_at DATETIME NOT NULL,
       study_activity_id INTEGER NOT NULL
   );
   ```

5. [ ] **create_table_study_activities.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS study_activities (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       study_session_id INTEGER,  -- or remove if not needed
       group_id INTEGER,          -- or remove if not needed
       created_at DATETIME
   );
   ```

6. [ ] **create_table_word_review_items.sql**  
   ```sql
   CREATE TABLE IF NOT EXISTS word_review_items (
       word_id INTEGER,
       study_session_id INTEGER,
       correct BOOLEAN,
       created_at DATETIME
   );
   ```

7. [ ] **(Optional)** create_table_word_reviews.sql  
   - If needed for a separate structure or relationships.

### One-Time Initialization vs. Setup Scripts

- [ ] **Run** each setup script in order using a simple Python script (or manually in the SQLite shell) to create your initial database schema.
- [ ] **Confirm** no errors occur when you run these scripts.

**Example** of a quick “init DB” script (if you are not yet using migrations):

```python
# init_db.py
import os
from lib.db import get_db_connection

def init_db():
    from glob import glob
    sql_files = sorted(glob("sql/setup/*.sql"))
    with get_db_connection() as conn:
        for f in sql_files:
            print(f"Applying {f}...")
            with open(f, "r") as sql_script:
                conn.executescript(sql_script.read())

if __name__ == "__main__":
    if os.path.exists("words.db"):
        os.remove("words.db")
    init_db()
    print("Database initialized successfully.")
```

Then:
```bash
python init_db.py
```

---

## Manual Migrations (No Alembic)

If you need to **add columns** or **modify tables** later, you can’t just rerun the initial scripts. Instead, you create separate migration scripts and a mechanism to track which have been applied.

### Steps

1. [ ] **Create** a `sql/migrations` folder.
2. [ ] **Create** a `schema_migrations` table to track applied migrations:
   ```sql
   -- This can be in 0001_init.sql or you can do it manually once
   CREATE TABLE IF NOT EXISTS schema_migrations (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       migration_name TEXT NOT NULL,
       applied_at DATETIME DEFAULT (datetime('now'))
   );
   ```
3. [ ] **Write** each migration in a file like `0002_add_parts_column_to_words.sql`:
   ```sql
   -- 0002_add_parts_column_to_words.sql
   ALTER TABLE words ADD COLUMN parts JSON;
   ```
   *(If you already have it, this is just an example for demonstration.)*

4. [ ] **Create** a `migrate.py` script to apply new migrations in ascending order:

   ```python
   import os
   from lib.db import get_db_connection

   MIGRATIONS_DIR = "sql/migrations"

   def get_applied_migrations():
       with get_db_connection() as conn:
           # Ensure table exists
           conn.execute("""
               CREATE TABLE IF NOT EXISTS schema_migrations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   migration_name TEXT NOT NULL,
                   applied_at DATETIME DEFAULT (datetime('now'))
               );
           """)
           rows = conn.execute("SELECT migration_name FROM schema_migrations").fetchall()
       return {row[0] for row in rows}

   def apply_migrations():
       applied = get_applied_migrations()
       # Sort by filename so we apply in correct sequence
       files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

       for file_name in files:
           if file_name not in applied:
               path = os.path.join(MIGRATIONS_DIR, file_name)
               with open(path, "r") as sql_file:
                   script = sql_file.read()
               with get_db_connection() as conn:
                   conn.executescript(script)
                   conn.execute("INSERT INTO schema_migrations (migration_name) VALUES (?)", (file_name,))
               print(f"Applied migration: {file_name}")

   if __name__ == "__main__":
       apply_migrations()
       print("All migrations applied successfully!")
   ```

5. [ ] (Optional) **Implement** rollback logic:  
   - Typically, you either create a `DOWN` script in each migration file or maintain a separate `.down.sql` file.  
   - If you need to revert, you run that `DOWN` script in reverse order.  
   - This can be more complex; decide if it’s necessary.

---

## Automated Testing Considerations

1. [ ] **Use** a separate **in-memory** or **temporary** SQLite DB when testing migrations:
   ```bash
   DB_NAME=":memory:" python -m pytest
   ```
   Or dynamically set `DB_NAME` in your test environment so you don’t overwrite your production/dev DB.
2. [ ] **Test** that migrations run **on a fresh DB** (no data), **and** test they run on a DB **with** an existing schema (to ensure no conflicts).
3. [ ] **Verify** that your final schema matches the expected state after all migrations have run.

### Example Test in `tests/test_migrations.py`

```python
import os
import pytest
from migrate import apply_migrations
from lib.db import DB_NAME, get_db_connection

@pytest.fixture
def temp_db():
    # Backup or remove existing DB
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    yield
    # Cleanup after tests
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def test_migrations_apply(temp_db):
    # Test applying all migrations to an empty DB
    apply_migrations()
    with get_db_connection() as conn:
        # Check if tables exist, for example:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
        assert cursor.fetchone() is not None, "Table 'words' should exist after migrations."
```

---

## Summary

1. **Set up** your raw SQLite connection in `lib/db.py`.  
2. **Store** table creation scripts in `sql/setup/`.  
3. **Optionally** create an `init_db.py` if you need a one-off script to create tables from scratch.  
4. **Maintain** a `sql/migrations` folder for manual incremental changes:
   - Each file named in ascending order (`0001_`, `0002_`, etc.).  
5. **Write** a `migrate.py` script to:
   - Track already applied migrations in a `schema_migrations` table.  
   - Apply new migration files in numerical order.  
6. **Test** your migration workflow, ensuring each script runs correctly on a fresh DB.

Following these steps and marking off the checkboxes as you go will provide a clean, maintainable approach to **creating**, **initializing**, and **migrating** your SQLite database using raw SQL and Python. 
```
