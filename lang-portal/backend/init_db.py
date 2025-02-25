import os
import json
from lib.db import get_db_connection

def init_db():
    from glob import glob
    sql_files = sorted(glob("sql/setup/*.sql"))
    with get_db_connection() as conn:
        for f in sql_files:
            print(f"Applying {f}...")
            with open(f, "r") as sql_script:
                conn.executescript(sql_script.read())
    print("Database tables created successfully.")

def seed_data():
    seed_files = {
        "words": "seed/words.json",
        "groups": "seed/groups.json",
        "word_groups": "seed/word_groups.json",
        "study_sessions": "seed/study_sessions.json",
        "study_activities": "seed/study_activities.json",
        "word_review_items": "seed/word_review_items.json"
    }

    with get_db_connection() as conn:
        # First seed the default settings if not exists
        conn.execute("""
            INSERT OR IGNORE INTO user_settings (
                id, words_per_session, review_interval,
                show_phonetics, show_usage_examples, dark_mode
            ) VALUES (
                1, 10, 24, 1, 1, 1
            )
        """)

        for table, file_path in seed_files.items():
            print(f"Seeding data for {table} from {file_path}...")
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                for entry in data:
                    # Convert JSON fields to strings
                    entry = {k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in entry.items()}
                    columns = ', '.join(entry.keys())
                    placeholders = ', '.join('?' * len(entry))
                    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                    conn.execute(sql, tuple(entry.values()))
    print("Database seeded successfully.")

if __name__ == "__main__":
    if os.path.exists("words.db"):
        os.remove("words.db")
    init_db()
    seed_data()
    print("Database initialized and seeded successfully.") 