import os
from lib.db import get_db_connection

MIGRATIONS_DIR = "sql/migrations"
ROLLBACK_DIR = "sql/migrations/down"

def get_applied_migrations(db_name):
    with get_db_connection(db_name) as conn:
        # Ensure the schema_migrations table exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT NOT NULL,
                applied_at DATETIME DEFAULT (datetime('now'))
            );
        """)
        rows = conn.execute("SELECT migration_name FROM schema_migrations").fetchall()
    return {row[0] for row in rows}

def apply_migrations(db_name="words.db"):
    applied = get_applied_migrations(db_name)
    # Sort by filename to apply in the correct sequence
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))

    with get_db_connection(db_name) as conn:
        for file_name in files:
            if file_name not in applied:
                path = os.path.join(MIGRATIONS_DIR, file_name)
                with open(path, "r") as sql_file:
                    script = sql_file.read()
                conn.executescript(script)
                conn.execute("INSERT INTO schema_migrations (migration_name) VALUES (?)", (file_name,))
                print(f"Applied migration: {file_name}")

def rollback_migration(db_name="words.db"):
    applied = get_applied_migrations(db_name)
    # Sort by filename to rollback in reverse order
    files = sorted(applied, reverse=True)

    with get_db_connection(db_name) as conn:
        for file_name in files:
            down_file = os.path.join(ROLLBACK_DIR, file_name)
            if os.path.exists(down_file):
                with open(down_file, "r") as sql_file:
                    script = sql_file.read()
                conn.executescript(script)
                conn.execute("DELETE FROM schema_migrations WHERE migration_name = ?", (file_name,))
                print(f"Rolled back migration: {file_name}")
                break  # Rollback one migration at a time

if __name__ == "__main__":
    import sys
    db_name = "words.db"
    if len(sys.argv) > 1:
        if sys.argv[1] == "rollback":
            rollback_migration(db_name)
        else:
            db_name = sys.argv[1]
    apply_migrations(db_name)
    print("Migration process completed.") 