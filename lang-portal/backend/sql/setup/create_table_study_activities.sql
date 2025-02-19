CREATE TABLE IF NOT EXISTS study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    study_session_id INTEGER,
    group_id INTEGER,
    created_at DATETIME
);