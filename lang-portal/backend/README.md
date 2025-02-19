# Backend Setup Guide

This guide provides instructions for setting up the backend, including initializing and seeding the database using `invoke`.

## Prerequisites

- Ensure you have Python 3.11+ installed.
- Install the required dependencies by running:
  ```bash
  pip install -r requirements.txt
  ```

## Database Initialization and Seeding

The backend uses SQLite for the database. You can initialize and seed the database using the `invoke` task runner.

### Available Tasks

1. **Initialize the Database:**
   - This task will create the database and all necessary tables.
   - Command:
     ```bash
     invoke initialize-db
     ```

2. **Seed the Database:**
   - This task will populate the database with initial data from JSON files.
   - Command:
     ```bash
     invoke seed-db
     ```

3. **Setup (Initialize and Seed):**
   - This task will perform both initialization and seeding in one step.
   - Command:
     ```bash
     invoke setup
     ```

### Running Tasks

- **Navigate** to the `lang-portal/backend` directory before running any tasks:
  ```bash
  cd lang-portal/backend
  ```

- Use the `invoke` command followed by the task name.

Example:
```bash
invoke setup
```

This will initialize the database and seed it with data, preparing it for use in the application.

## Additional Information

- Ensure that the `words.db` file is not in version control by adding it to `.gitignore`.
- The database schema and seed data are defined in the `sql/setup` and `seed` directories, respectively.

For further details, refer to the specific documentation files within the project.

# Language Portal Backend

This backend provides an API for managing language learning resources using FastAPI.

## Prerequisites

- Python 3.11+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Running the FastAPI Application

To start the FastAPI server, use the following command:

```bash
cd lang-portal/backend
uvicorn app:app --reload
```

- The server will be available at `http://127.0.0.1:8000`.
- Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Testing the `get_words` Endpoint

You can test the `get_words` endpoint using `curl`:

```bash
curl -X GET "http://127.0.0.1:8000/api/words"
```

- This will return a paginated list of words.
- You can specify the page and page size using query parameters:
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/words?page=2&page_size=5"
  ```

## Running Unit Tests

To run the unit tests, use `pytest`:

```bash
pytest tests -v
```

- This will execute all tests in the `tests` directory.
- Ensure that the database is set up correctly before running tests.

## Additional Information

- The API uses CORS middleware to allow requests from any origin.
- The `get_words` endpoint supports pagination and returns data in a structured format using Pydantic models. 