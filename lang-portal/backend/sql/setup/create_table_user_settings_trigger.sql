-- Trigger to update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS user_settings_updated_at 
AFTER UPDATE ON user_settings
BEGIN
    UPDATE user_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END; 