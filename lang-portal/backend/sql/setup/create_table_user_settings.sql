CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY,
    words_per_session INTEGER NOT NULL DEFAULT 10,
    review_interval INTEGER NOT NULL DEFAULT 24,
    show_phonetics BOOLEAN NOT NULL DEFAULT 1,
    show_usage_examples BOOLEAN NOT NULL DEFAULT 1,
    dark_mode BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS user_settings_updated_at 
AFTER UPDATE ON user_settings
BEGIN
    UPDATE user_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Insert default settings
INSERT OR IGNORE INTO user_settings (id) VALUES (1); 