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

## API Endpoints

### Words Endpoints

1. **Get All Words with Pagination:**
   - **Endpoint:** `GET /api/words`
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/words?page=1&page_size=10"
     ```

2. **Get a Specific Word by ID:**
   - **Endpoint:** `GET /api/words/{word_id}`
   - **Path Parameter:**
     - `word_id`: The ID of the word to retrieve.
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/words/1"
     ```

### Groups Endpoints

1. **Get All Groups with Pagination:**
   - **Endpoint:** `GET /api/groups`
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/groups?page=1&page_size=10"
     ```

2. **Get a Specific Group by ID:**
   - **Endpoint:** `GET /api/groups/{group_id}`
   - **Path Parameter:**
     - `group_id`: The ID of the group to retrieve.
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/groups/1"
     ```

3. **Get Words for a Specific Group with Pagination:**
   - **Endpoint:** `GET /api/groups/{group_id}/words`
   - **Path Parameter:**
     - `group_id`: The ID of the group to retrieve words for.
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/groups/1/words?page=1&page_size=10"
     ```

4. **Get Study Sessions for a Specific Group with Pagination:**
   - **Endpoint:** `GET /api/groups/{group_id}/study_sessions`
   - **Path Parameter:**
     - `group_id`: The ID of the group to retrieve study sessions for.
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     curl -X GET "http://127.0.0.1:8000/api/groups/1/study_sessions?page=1&page_size=10"
     ```

### Study Activities Endpoints

1. **Get a Specific Study Activity by ID:**
   - **Endpoint:** `GET /api/study_activities/{activity_id}`
   - **Path Parameter:**
     - `activity_id`: The ID of the study activity to retrieve.
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/study_activities/1"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/study_activities/1" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "id": 1,
       "name": "Vocabulary Review",
       "study_session_id": 1,
       "group_id": 1,
       "created_at": "2024-02-18T10:00:00",
       "group_name": "Beginner Patois",
       "review_items_count": 10
     }
     ```

2. **Get Study Sessions for a Specific Study Activity with Pagination:**
   - **Endpoint:** `GET /api/study_activities/{activity_id}/study_sessions`
   - **Path Parameter:**
     - `activity_id`: The ID of the study activity to retrieve study sessions for.
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/study_activities/1/study_sessions"
     
     # With pagination
     curl -X GET "http://127.0.0.1:8000/api/study_activities/1/study_sessions?page=1&page_size=5"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/study_activities/1/study_sessions" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "study_sessions": [
         {
           "id": 1,
           "activity_name": "Vocabulary Review",
           "group_name": "Beginner Patois",
           "start_time": "2024-02-18T10:00:00",
           "end_time": null,
           "review_items_count": 10
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 1,
         "items_per_page": 10
       }
     }
     ```

3. **Create a New Study Activity and Start Session:**
   - **Endpoint:** `POST /api/study_activities`
   - **Request Body:**
     ```json
     {
       "name": "Vocabulary Review",
       "group_id": 1
     }
     ```
   - **Example:**
     ```bash
     # Create a new study activity
     curl -X POST "http://127.0.0.1:8000/api/study_activities" \
       -H "Content-Type: application/json" \
       -d '{"name": "Vocabulary Review", "group_id": 1}'
     
     # Pretty print JSON response
     curl -X POST "http://127.0.0.1:8000/api/study_activities" \
       -H "Content-Type: application/json" \
       -d '{"name": "Vocabulary Review", "group_id": 1}' | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "id": 21,
       "name": "Vocabulary Review",
       "study_session_id": 21,
       "group_id": 1,
       "created_at": "2024-02-19T15:30:00",
       "group_name": "Beginner Patois",
       "review_items_count": 0
     }
     ```

### Study Sessions Endpoints

1. **Get All Study Sessions with Pagination:**
   - **Endpoint:** `GET /api/study_sessions`
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/study_sessions"
     
     # With pagination
     curl -X GET "http://127.0.0.1:8000/api/study_sessions?page=1&page_size=5"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/study_sessions" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "study_sessions": [
         {
           "id": 1,
           "activity_name": "Vocabulary Review",
           "group_name": "Beginner Patois",
           "start_time": "2024-02-18T10:00:00",
           "end_time": null,
           "review_items_count": 10
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 1,
         "items_per_page": 10
       }
     }
     ```

2. **Get a Specific Study Session by ID:**
   - **Endpoint:** `GET /api/study_sessions/{session_id}`
   - **Path Parameter:**
     - `session_id`: The ID of the study session to retrieve.
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/study_sessions/1"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/study_sessions/1" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "id": 1,
       "activity_name": "Vocabulary Review",
       "group_name": "Beginner Patois",
       "start_time": "2024-02-18T10:00:00",
       "end_time": null,
       "review_items_count": 10
     }
     ```

3. **Get Words for a Specific Study Session with Pagination:**
   - **Endpoint:** `GET /api/study_sessions/{session_id}/words`
   - **Path Parameter:**
     - `session_id`: The ID of the study session to retrieve words for.
   - **Query Parameters:**
     - `page`: The page number to retrieve (default: 1).
     - `page_size`: The number of items per page (default: 10).
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/study_sessions/1/words"
     
     # With pagination
     curl -X GET "http://127.0.0.1:8000/api/study_sessions/1/words?page=1&page_size=5"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/study_sessions/1/words" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "words": [
         {
           "id": 1,
           "jamaican_patois": "mi",
           "english": "me/my",
           "parts": {
             "type": "pronoun",
             "usage": "subject"
           },
           "correct_count": 5,
           "wrong_count": 1
         }
       ],
       "pagination": {
         "current_page": 1,
         "total_pages": 1,
         "total_items": 1,
         "items_per_page": 10
       }
     }
     ```

4. **Record a Word Review:**
   - **Endpoint:** `POST /api/study_sessions/{session_id}/words/{word_id}/review`
   - **Path Parameters:**
     - `session_id`: The ID of the study session.
     - `word_id`: The ID of the word being reviewed.
   - **Request Body:**
     ```json
     {
       "correct": true
     }
     ```
   - **Example:**
     ```bash
     # Create a word review
     curl -X POST "http://127.0.0.1:8000/api/study_sessions/1/words/1/review" \
       -H "Content-Type: application/json" \
       -d '{"correct": true}'
     
     # Pretty print JSON response
     curl -X POST "http://127.0.0.1:8000/api/study_sessions/1/words/1/review" \
       -H "Content-Type: application/json" \
       -d '{"correct": true}' | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "id": 1,
       "word_id": 1,
       "study_session_id": 1,
       "correct": true,
       "created_at": "2024-02-19T15:30:00",
       "word_jamaican_patois": "mi",
       "word_english": "me/my"
     }
     ```

### Dashboard Endpoints

1. **Get Last Study Session:**
   - **Endpoint:** `GET /api/dashboard/last_study_session`
   - **Description:** Retrieve information about the most recent study session.
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/dashboard/last_study_session"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/dashboard/last_study_session" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "id": 1,
       "activity_name": "Vocabulary Review",
       "group_name": "Beginner Patois",
       "start_time": "2024-02-18T10:00:00",
       "end_time": null,
       "review_items_count": 10
     }
     ```

2. **Get Study Progress Statistics:**
   - **Endpoint:** `GET /api/dashboard/study_progress`
   - **Description:** Retrieve overall study progress statistics including word reviews, accuracy rates, and group-specific progress.
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/dashboard/study_progress"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/dashboard/study_progress" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "total_words_reviewed": 150,
       "total_correct": 120,
       "total_incorrect": 30,
       "accuracy_rate": 80.0,
       "total_study_sessions": 10,
       "total_study_time_minutes": 120,
       "words_by_group": [
         {
           "group_id": 1,
           "group_name": "Beginner Patois",
           "unique_words": 50,
           "total_reviews": 75,
           "correct_reviews": 60,
           "accuracy_rate": 80.0
         }
       ]
     }
     ```

3. **Get Quick Statistics:**
   - **Endpoint:** `GET /api/dashboard/quick-stats`
   - **Description:** Retrieve quick overview statistics for the dashboard.
   - **Example:**
     ```bash
     # Basic request
     curl -X GET "http://127.0.0.1:8000/api/dashboard/quick-stats"
     
     # Pretty print JSON response
     curl -X GET "http://127.0.0.1:8000/api/dashboard/quick-stats" | python -m json.tool
     ```
   - **Response Example:**
     ```json
     {
       "total_words": 200,
       "words_learned": 75,
       "total_study_time_minutes": 180,
       "recent_accuracy": 85.5,
       "streak_days": 3
     }
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
- The endpoints support pagination and return data in a structured format using Pydantic models.

## Testing with Postman

The API includes a Postman collection file (`lang-portal.postman_collection.json`) that contains all endpoints for testing.

### Importing the Collection

1. Open Postman
2. Click the "Import" button in the top left
3. Drag and drop the `lang-portal.postman_collection.json` file or click "Upload Files" to select it
4. Click "Import" to add the collection to your workspace

### Collection Structure

The collection is organized into four main folders:

1. **Groups**
   - Get All Groups
   - Get Group by ID
   - Get Group Words
   - Get Group Study Sessions

2. **Study Activities**
   - Create Study Activity
   - Get Study Activity by ID

3. **Study Sessions**
   - Get All Study Sessions
   - Get Study Session by ID
   - Get Session Words
   - Create Word Review

4. **Dashboard**
   - Get Last Study Session
   - Get Study Progress
   - Get Quick Stats

### Using the Collection

1. Make sure your FastAPI server is running at `http://127.0.0.1:8000`
2. All endpoints are pre-configured with:
   - Correct HTTP methods
   - Required headers
   - Example request bodies for POST requests
   - Query parameters for pagination
3. For endpoints with path parameters (like `{id}`), replace the sample IDs with actual values
4. Click "Send" to make the request

### Example Usage

1. **Create a Study Activity:**
   - Open the "Study Activities" folder
   - Select "Create Study Activity"
   - The request body is pre-filled with:
     ```json
     {
       "name": "Vocabulary Review",
       "group_id": 1
     }
     ```
   - Click "Send" to create the activity

2. **View Study Progress:**
   - Open the "Dashboard" folder
   - Select "Get Study Progress"
   - Click "Send" to view overall progress statistics

### Tips

- Use the "Pretty" response formatter in Postman to view formatted JSON responses
- Check the "Headers" tab to verify Content-Type is set correctly
- For paginated endpoints, try different page and page_size values in the query parameters 

## Testing with Thunder Client

The API includes a Thunder Client collection file (`thunder-collection.json`) for VS Code users who prefer Thunder Client over Postman.

### Setting Up Thunder Client

1. Install the Thunder Client extension in VS Code
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Thunder Client"
   - Click Install

### Importing the Collection

1. Open Thunder Client in VS Code
   - Click the Thunder Client icon in the activity bar
   - Or use the shortcut (Ctrl+Shift+P and search "Thunder Client")
2. Click on "Collections" in the Thunder Client sidebar
3. Click the "Import" button (or use the menu)
4. Select the `thunder-collection.json` file
5. The collection will be imported with all endpoints ready to test

### Collection Structure

The collection mirrors the Postman collection structure with four main folders:

1. **Groups**
   - Get All Groups
   - Get Group by ID
   - Get Group Words
   - Get Group Study Sessions

2. **Study Activities**
   - Create Study Activity
   - Get Study Activity by ID

3. **Study Sessions**
   - Get All Study Sessions
   - Get Study Session by ID
   - Get Session Words
   - Create Word Review

4. **Dashboard**
   - Get Last Study Session
   - Get Study Progress
   - Get Quick Stats

### Using the Collection

1. Ensure your FastAPI server is running at `http://127.0.0.1:8000`
2. In Thunder Client:
   - Click on any request in the collection
   - The request details will appear in the main panel
   - Click "Send" to execute the request

### Example Usage

1. **Testing a POST Request:**
   - Open "Study Activities" → "Create Study Activity"
   - The request body is pre-configured:
     ```json
     {
       "name": "Vocabulary Review",
       "group_id": 1
     }
     ```
   - Click "Send" to execute

2. **Testing with Query Parameters:**
   - Open any paginated endpoint (e.g., "Get All Groups")
   - The URL includes default pagination: `?page=1&page_size=10`
   - Modify these values as needed
   - Click "Send" to test with different pagination

### Tips

- Use the "Preview" tab to see formatted JSON responses
- The "Headers" tab shows all request headers
- For POST requests, check the "Body" tab for the correct JSON structure
- Use the "Query" tab to modify URL parameters easily 