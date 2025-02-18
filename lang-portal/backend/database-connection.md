# Database Connection Setup

This document outlines the steps taken to set up and test the SQLite database connection for the language learning portal.

## Setup Steps

1. **Create Database Connection:**
   - Implemented a context manager in `lib/db.py` to handle SQLite connections.

2. **Dependencies:**
   - Added necessary dependencies to `requirements.txt` (excluding `sqlite3` as it's part of Python's standard library).

3. **Test Connection:**
   - Created a script `test_db_connection.py` to verify the database connection.

## Testing

### Test the Connection Script

- **Command to Test Connection:**
  ```bash
  python lang-portal/backend/test_db_connection.py
  ```

- **Expected Output:**
  - "Opened database successfully!" indicates a successful connection.

### Run Unit Test

- **Command to Run Unit Test:**
  ```bash
  python -m unittest lang-portal/backend/tests/test_db.py
  ```

- **Expected Output:**
  - "Database connection test passed." indicates the unit test was successful. 