CREATE TABLE IF NOT EXISTS word_review_items (
    word_id INTEGER,
    study_session_id INTEGER,
    correct BOOLEAN,
    created_at DATETIME
);