from lib.db import get_db_connection

def test_connection():
    with get_db_connection() as conn:
        print("Opened database successfully!")

if __name__ == "__main__":
    test_connection() 