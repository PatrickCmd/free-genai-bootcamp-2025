Below are **six** example JSON seed files—one for each major table in the specs—with **20** records apiece. Each file is kept **atomic** (i.e., independently seedable). Adjust the `id` values, timestamps, or text as needed.

---

## 1. `words.json`
```json
[
  {
    "id": 1,
    "jamaican_patois": "Wah Gwaan",
    "english": "Hello",
    "parts": { "type": "phrase" }
  },
  {
    "id": 2,
    "jamaican_patois": "Mi deh yah",
    "english": "I'm here",
    "parts": { "type": "phrase" }
  },
  {
    "id": 3,
    "jamaican_patois": "Weh yuh deh pon?",
    "english": "What are you up to?",
    "parts": { "type": "phrase" }
  },
  {
    "id": 4,
    "jamaican_patois": "Small up yuhself",
    "english": "Make room",
    "parts": { "type": "phrase" }
  },
  {
    "id": 5,
    "jamaican_patois": "Tek time",
    "english": "Go slowly",
    "parts": { "type": "phrase" }
  },
  {
    "id": 6,
    "jamaican_patois": "Big up",
    "english": "Respect",
    "parts": { "type": "verb" }
  },
  {
    "id": 7,
    "jamaican_patois": "Likkle more",
    "english": "Later",
    "parts": { "type": "phrase" }
  },
  {
    "id": 8,
    "jamaican_patois": "Fimi",
    "english": "Mine",
    "parts": { "type": "possessive" }
  },
  {
    "id": 9,
    "jamaican_patois": "Nuh badda mi",
    "english": "Don't bother me",
    "parts": { "type": "phrase" }
  },
  {
    "id": 10,
    "jamaican_patois": "Craven",
    "english": "Greedy",
    "parts": { "type": "adjective" }
  },
  {
    "id": 11,
    "jamaican_patois": "Madda",
    "english": "Mother",
    "parts": { "type": "noun" }
  },
  {
    "id": 12,
    "jamaican_patois": "Fada",
    "english": "Father",
    "parts": { "type": "noun" }
  },
  {
    "id": 13,
    "jamaican_patois": "Pickney",
    "english": "Child",
    "parts": { "type": "noun" }
  },
  {
    "id": 14,
    "jamaican_patois": "Nyam",
    "english": "Eat",
    "parts": { "type": "verb" }
  },
  {
    "id": 15,
    "jamaican_patois": "Rhaatid",
    "english": "Expression of surprise",
    "parts": { "type": "interjection" }
  },
  {
    "id": 16,
    "jamaican_patois": "Boonoonoonoos",
    "english": "Wonderful",
    "parts": { "type": "adjective" }
  },
  {
    "id": 17,
    "jamaican_patois": "Bredren",
    "english": "Friend (male)",
    "parts": { "type": "noun" }
  },
  {
    "id": 18,
    "jamaican_patois": "Sistren",
    "english": "Friend (female)",
    "parts": { "type": "noun" }
  },
  {
    "id": 19,
    "jamaican_patois": "Yute",
    "english": "Youth",
    "parts": { "type": "noun" }
  },
  {
    "id": 20,
    "jamaican_patois": "Irie",
    "english": "Alright / Good",
    "parts": { "type": "adjective" }
  }
]
```

---

## 2. `groups.json`
```json
[
  { "id": 1,  "name": "Basic Greetings" },
  { "id": 2,  "name": "Common Phrases" },
  { "id": 3,  "name": "Food & Eating" },
  { "id": 4,  "name": "Daily Expressions" },
  { "id": 5,  "name": "Verbs Collection" },
  { "id": 6,  "name": "Adjective Bunch" },
  { "id": 7,  "name": "Slang Terms" },
  { "id": 8,  "name": "Nature & Weather" },
  { "id": 9,  "name": "Travel & Directions" },
  { "id": 10, "name": "Time & Dates" },
  { "id": 11, "name": "Numbers" },
  { "id": 12, "name": "Animals" },
  { "id": 13, "name": "Emotions & Feelings" },
  { "id": 14, "name": "Colors" },
  { "id": 15, "name": "Hobbies" },
  { "id": 16, "name": "Shopping" },
  { "id": 17, "name": "Health & Body" },
  { "id": 18, "name": "Festivals & Events" },
  { "id": 19, "name": "Music & Dance" },
  { "id": 20, "name": "Random" }
]
```

---

## 3. `word_groups.json`
A **many-to-many** relationship. Below is a simple example linking each `word_id` to a matching `group_id` (1→1, 2→2, etc.). Adjust to your needs.

```json
[
  { "id": 1,  "word_id": 1,  "group_id": 1 },
  { "id": 2,  "word_id": 2,  "group_id": 2 },
  { "id": 3,  "word_id": 3,  "group_id": 3 },
  { "id": 4,  "word_id": 4,  "group_id": 4 },
  { "id": 5,  "word_id": 5,  "group_id": 5 },
  { "id": 6,  "word_id": 6,  "group_id": 6 },
  { "id": 7,  "word_id": 7,  "group_id": 7 },
  { "id": 8,  "word_id": 8,  "group_id": 8 },
  { "id": 9,  "word_id": 9,  "group_id": 9 },
  { "id": 10, "word_id": 10, "group_id": 10 },
  { "id": 11, "word_id": 11, "group_id": 11 },
  { "id": 12, "word_id": 12, "group_id": 12 },
  { "id": 13, "word_id": 13, "group_id": 13 },
  { "id": 14, "word_id": 14, "group_id": 14 },
  { "id": 15, "word_id": 15, "group_id": 15 },
  { "id": 16, "word_id": 16, "group_id": 16 },
  { "id": 17, "word_id": 17, "group_id": 17 },
  { "id": 18, "word_id": 18, "group_id": 18 },
  { "id": 19, "word_id": 19, "group_id": 19 },
  { "id": 20, "word_id": 20, "group_id": 20 }
]
```

---

## 4. `study_sessions.json`
Each **study_session** has an `id`, `group_id`, `created_at`, and `study_activity_id`. Below is an example.

```json
[
  {
    "id": 1,
    "group_id": 1,
    "created_at": "2025-02-02T12:00:00Z",
    "study_activity_id": 1
  },
  {
    "id": 2,
    "group_id": 2,
    "created_at": "2025-02-03T12:00:00Z",
    "study_activity_id": 2
  },
  {
    "id": 3,
    "group_id": 3,
    "created_at": "2025-02-04T12:00:00Z",
    "study_activity_id": 3
  },
  {
    "id": 4,
    "group_id": 4,
    "created_at": "2025-02-05T12:00:00Z",
    "study_activity_id": 4
  },
  {
    "id": 5,
    "group_id": 5,
    "created_at": "2025-02-06T12:00:00Z",
    "study_activity_id": 5
  },
  {
    "id": 6,
    "group_id": 6,
    "created_at": "2025-02-07T12:00:00Z",
    "study_activity_id": 6
  },
  {
    "id": 7,
    "group_id": 7,
    "created_at": "2025-02-08T12:00:00Z",
    "study_activity_id": 7
  },
  {
    "id": 8,
    "group_id": 8,
    "created_at": "2025-02-09T12:00:00Z",
    "study_activity_id": 8
  },
  {
    "id": 9,
    "group_id": 9,
    "created_at": "2025-02-10T12:00:00Z",
    "study_activity_id": 9
  },
  {
    "id": 10,
    "group_id": 10,
    "created_at": "2025-02-11T12:00:00Z",
    "study_activity_id": 10
  },
  {
    "id": 11,
    "group_id": 11,
    "created_at": "2025-02-12T12:00:00Z",
    "study_activity_id": 11
  },
  {
    "id": 12,
    "group_id": 12,
    "created_at": "2025-02-13T12:00:00Z",
    "study_activity_id": 12
  },
  {
    "id": 13,
    "group_id": 13,
    "created_at": "2025-02-14T12:00:00Z",
    "study_activity_id": 13
  },
  {
    "id": 14,
    "group_id": 14,
    "created_at": "2025-02-15T12:00:00Z",
    "study_activity_id": 14
  },
  {
    "id": 15,
    "group_id": 15,
    "created_at": "2025-02-16T12:00:00Z",
    "study_activity_id": 15
  },
  {
    "id": 16,
    "group_id": 16,
    "created_at": "2025-02-17T12:00:00Z",
    "study_activity_id": 16
  },
  {
    "id": 17,
    "group_id": 17,
    "created_at": "2025-02-18T12:00:00Z",
    "study_activity_id": 17
  },
  {
    "id": 18,
    "group_id": 18,
    "created_at": "2025-02-19T12:00:00Z",
    "study_activity_id": 18
  },
  {
    "id": 19,
    "group_id": 19,
    "created_at": "2025-02-20T12:00:00Z",
    "study_activity_id": 19
  },
  {
    "id": 20,
    "group_id": 20,
    "created_at": "2025-02-21T12:00:00Z",
    "study_activity_id": 20
  }
]
```

---

## 5. `study_activities.json`
This might contain columns like `id`, `study_session_id`, `group_id`, `created_at`. (Exact columns depend on your schema.)

```json
[
  {
    "id": 1,
    "study_session_id": 1,
    "group_id": 1,
    "created_at": "2025-02-02T13:00:00Z"
  },
  {
    "id": 2,
    "study_session_id": 2,
    "group_id": 2,
    "created_at": "2025-02-03T13:00:00Z"
  },
  {
    "id": 3,
    "study_session_id": 3,
    "group_id": 3,
    "created_at": "2025-02-04T13:00:00Z"
  },
  {
    "id": 4,
    "study_session_id": 4,
    "group_id": 4,
    "created_at": "2025-02-05T13:00:00Z"
  },
  {
    "id": 5,
    "study_session_id": 5,
    "group_id": 5,
    "created_at": "2025-02-06T13:00:00Z"
  },
  {
    "id": 6,
    "study_session_id": 6,
    "group_id": 6,
    "created_at": "2025-02-07T13:00:00Z"
  },
  {
    "id": 7,
    "study_session_id": 7,
    "group_id": 7,
    "created_at": "2025-02-08T13:00:00Z"
  },
  {
    "id": 8,
    "study_session_id": 8,
    "group_id": 8,
    "created_at": "2025-02-09T13:00:00Z"
  },
  {
    "id": 9,
    "study_session_id": 9,
    "group_id": 9,
    "created_at": "2025-02-10T13:00:00Z"
  },
  {
    "id": 10,
    "study_session_id": 10,
    "group_id": 10,
    "created_at": "2025-02-11T13:00:00Z"
  },
  {
    "id": 11,
    "study_session_id": 11,
    "group_id": 11,
    "created_at": "2025-02-12T13:00:00Z"
  },
  {
    "id": 12,
    "study_session_id": 12,
    "group_id": 12,
    "created_at": "2025-02-13T13:00:00Z"
  },
  {
    "id": 13,
    "study_session_id": 13,
    "group_id": 13,
    "created_at": "2025-02-14T13:00:00Z"
  },
  {
    "id": 14,
    "study_session_id": 14,
    "group_id": 14,
    "created_at": "2025-02-15T13:00:00Z"
  },
  {
    "id": 15,
    "study_session_id": 15,
    "group_id": 15,
    "created_at": "2025-02-16T13:00:00Z"
  },
  {
    "id": 16,
    "study_session_id": 16,
    "group_id": 16,
    "created_at": "2025-02-17T13:00:00Z"
  },
  {
    "id": 17,
    "study_session_id": 17,
    "group_id": 17,
    "created_at": "2025-02-18T13:00:00Z"
  },
  {
    "id": 18,
    "study_session_id": 18,
    "group_id": 18,
    "created_at": "2025-02-19T13:00:00Z"
  },
  {
    "id": 19,
    "study_session_id": 19,
    "group_id": 19,
    "created_at": "2025-02-20T13:00:00Z"
  },
  {
    "id": 20,
    "study_session_id": 20,
    "group_id": 20,
    "created_at": "2025-02-21T13:00:00Z"
  }
]
```

---

## 6. `word_review_items.json`
Table columns: `word_id`, `study_session_id`, `correct`, `created_at`.  
Below is a simple pattern: even entries are `correct: true`, odd are `correct: false`.

```json
[
  {
    "word_id": 1,
    "study_session_id": 1,
    "correct": false,
    "created_at": "2025-02-02T14:00:00Z"
  },
  {
    "word_id": 2,
    "study_session_id": 2,
    "correct": true,
    "created_at": "2025-02-03T14:00:00Z"
  },
  {
    "word_id": 3,
    "study_session_id": 3,
    "correct": false,
    "created_at": "2025-02-04T14:00:00Z"
  },
  {
    "word_id": 4,
    "study_session_id": 4,
    "correct": true,
    "created_at": "2025-02-05T14:00:00Z"
  },
  {
    "word_id": 5,
    "study_session_id": 5,
    "correct": false,
    "created_at": "2025-02-06T14:00:00Z"
  },
  {
    "word_id": 6,
    "study_session_id": 6,
    "correct": true,
    "created_at": "2025-02-07T14:00:00Z"
  },
  {
    "word_id": 7,
    "study_session_id": 7,
    "correct": false,
    "created_at": "2025-02-08T14:00:00Z"
  },
  {
    "word_id": 8,
    "study_session_id": 8,
    "correct": true,
    "created_at": "2025-02-09T14:00:00Z"
  },
  {
    "word_id": 9,
    "study_session_id": 9,
    "correct": false,
    "created_at": "2025-02-10T14:00:00Z"
  },
  {
    "word_id": 10,
    "study_session_id": 10,
    "correct": true,
    "created_at": "2025-02-11T14:00:00Z"
  },
  {
    "word_id": 11,
    "study_session_id": 11,
    "correct": false,
    "created_at": "2025-02-12T14:00:00Z"
  },
  {
    "word_id": 12,
    "study_session_id": 12,
    "correct": true,
    "created_at": "2025-02-13T14:00:00Z"
  },
  {
    "word_id": 13,
    "study_session_id": 13,
    "correct": false,
    "created_at": "2025-02-14T14:00:00Z"
  },
  {
    "word_id": 14,
    "study_session_id": 14,
    "correct": true,
    "created_at": "2025-02-15T14:00:00Z"
  },
  {
    "word_id": 15,
    "study_session_id": 15,
    "correct": false,
    "created_at": "2025-02-16T14:00:00Z"
  },
  {
    "word_id": 16,
    "study_session_id": 16,
    "correct": true,
    "created_at": "2025-02-17T14:00:00Z"
  },
  {
    "word_id": 17,
    "study_session_id": 17,
    "correct": false,
    "created_at": "2025-02-18T14:00:00Z"
  },
  {
    "word_id": 18,
    "study_session_id": 18,
    "correct": true,
    "created_at": "2025-02-19T14:00:00Z"
  },
  {
    "word_id": 19,
    "study_session_id": 19,
    "correct": false,
    "created_at": "2025-02-20T14:00:00Z"
  },
  {
    "word_id": 20,
    "study_session_id": 20,
    "correct": true,
    "created_at": "2025-02-21T14:00:00Z"
  }
]
```

---

### Usage Notes

1. **Seeding**:  
   - Your seeding script (e.g., `seed_data.py`) can read these JSON files, parse them, and insert rows via raw `INSERT` statements into each table.  
   - Ensure the table structure matches these fields (some tables auto-increment `id`, so you might omit `"id"` in your inserts if the DB sets it).  

2. **Atomic**:  
   - Because each JSON file contains data for exactly one table, you can seed them in **any** order or just the ones you need.  
   - This structure is easy to maintain or replace individually.  

3. **Adjust**:  
   - If your actual schema differs (e.g., extra columns or different field names), update these JSONs accordingly.  