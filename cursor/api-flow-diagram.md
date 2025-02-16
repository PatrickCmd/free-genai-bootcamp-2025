Below is a **Mermaid** file (`api_flow.mmd`) illustrating a **high-level API flow** using a **sequence diagram**. It covers a few core endpoints from client → backend → database, then back to the client with JSON responses. You can modify or expand this based on your exact workflow.

```mermaid
---
title: API Flow Sequence Diagram
---

sequenceDiagram
    participant Client as User/Client
    participant Server as FastAPI Backend
    participant DB as SQLite DB

    %% ----------------------------
    %% DASHBOARD ENDPOINTS
    %% ----------------------------
    Client->>Server: GET /api/dashboard/last_study_session
    Server->>DB: SELECT the most recent study_session
    DB-->>Server: returns row
    Server-->>Client: JSON with { "id": ..., "group_id": ..., ... }

    Client->>Server: GET /api/dashboard/study_progress
    Server->>DB: SELECT counts for total words studied & total words
    DB-->>Server: returns counts
    Server-->>Client: JSON with { "total_words_studied": ..., "total_available_words": ... }

    Client->>Server: GET /api/dashboard/quick-stats
    Server->>DB: SELECT success rate, session count, etc.
    DB-->>Server: returns calculated stats
    Server-->>Client: JSON with { "success_rate": ..., "total_study_sessions": ... }

    Note over Client: Dashboard is updated with stats.

    %% ----------------------------
    %% WORDS ENDPOINTS
    %% ----------------------------
    Client->>Server: GET /api/words?page=1
    Server->>DB: SELECT words with LIMIT/OFFSET
    DB-->>Server: returns rows
    Server-->>Client: JSON array of words + pagination

    Client->>Server: GET /api/words/1
    Server->>DB: SELECT word #1 details, stats, groups
    DB-->>Server: returns row, stats, group membership
    Server-->>Client: JSON with word + stats + groups

    Note over Client: Client displays word info.

    %% ----------------------------
    %% GROUPS ENDPOINTS
    %% ----------------------------
    Client->>Server: GET /api/groups?page=1
    Server->>DB: SELECT groups with pagination
    DB-->>Server: returns group rows
    Server-->>Client: JSON array of groups + pagination

    Client->>Server: GET /api/groups/1/words
    Server->>DB: SELECT words belonging to group #1
    DB-->>Server: returns matching word rows
    Server-->>Client: JSON word list

    Note over Client: Client displays words for that group.

    %% ----------------------------
    %% STUDY SESSIONS ENDPOINTS
    %% ----------------------------
    Client->>Server: POST /api/study_activities { "group_id": ..., "study_activity_id": ... }
    Server->>DB: INSERT new study_session (and possibly study_activity)
    DB-->>Server: returns new session_id
    Server-->>Client: { "id": 123, "group_id": ... }

    Note over Client: Client navigates user into new study session.

    Client->>Server: POST /api/study_sessions/123/words/5/review { "correct": true }
    Server->>DB: INSERT into word_review_items (word_id=5, session_id=123, correct=1)
    DB-->>Server: ok
    Server-->>Client: { "success": true, "word_id": 5, ... }

    %% ----------------------------
    %% RESET ENDPOINTS
    %% ----------------------------
    Client->>Server: POST /api/reset_history
    Server->>DB: DELETE FROM study_sessions, word_review_items
    DB-->>Server: success
    Server-->>Client: { "success": true, "message": "Study history has been reset" }

    Client->>Server: POST /api/full_reset
    Server->>DB: DELETE from all main tables
    DB-->>Server: success
    Server-->>Client: { "success": true, "message": "System has been fully reset" }
```

### How to Use

1. **Save** the above snippet to a file named `api_flow.mmd`.
2. **Render** it via your favorite Mermaid renderer or an online [Mermaid Live Editor](https://mermaid.live/).
3. **Extend** or **modify** the sequence diagram to show additional detail (e.g., error cases, authentication steps, etc.) if needed.