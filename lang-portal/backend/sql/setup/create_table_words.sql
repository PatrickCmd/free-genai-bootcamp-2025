CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jamaican_patois TEXT NOT NULL,
    english TEXT NOT NULL,
    parts JSON
);