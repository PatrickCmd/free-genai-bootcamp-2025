Below is a high-level **step-by-step plan** for building a **React + TypeScript + Tailwind CSS + Vite** front-end app that implements all the pages and components specified in the **Front-End Technical Specs**. The plan uses **atomic tasks**, helping a junior dev focus on **one component at a time**.

---

## Table of Contents

1. [Project Initialization](#1-project-initialization)  
2. [Global Setup (Layout, Router, Tailwind)](#2-global-setup-layout-router-tailwind)  
3. [Dashboard Page (`/dashboard`)](#3-dashboard-page-dashboard)  
4. [Study Activities Index (`/study_activities`)](#4-study-activities-index-study_activities)  
5. [Study Activity Show (`/study_activities/:id`)](#5-study-activity-show-study_activitiesid)  
6. [Study Activity Launch (`/study_activities/:id/launch`)](#6-study-activity-launch-study_activitiesidlaunch)  
7. [Words Index (`/words`)](#7-words-index-words)  
8. [Word Show (`/words/:id`)](#8-word-show-wordsid)  
9. [Word Groups Index (`/groups`)](#9-word-groups-index-groups)  
10. [Group Show (`/groups/:id`)](#10-group-show-groupsid)  
11. [Study Sessions Index (`/study_sessions`)](#11-study-sessions-index-study_sessions)  
12. [Study Session Show (`/study_sessions/:id`)](#12-study-session-show-study_sessionsid)  
13. [Settings Page (`/settings`)](#13-settings-page-settings)  
14. [Testing and Final Review](#14-testing-and-final-review)

---

## 1. Project Initialization

1. [x] **Create** a new Vite + React + TypeScript project:
   ```bash
   npm create vite@latest lang-portal-frontend -- --template react-ts
   cd lang-portal-frontend
   npm install
   ```
2. [x] **Install** Tailwind CSS:
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
3. [x] **Configure** `tailwind.config.js`:
   ```js
   /** @type {import('tailwindcss').Config} */
   export default {
     content: [
       "./index.html",
       "./src/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```
4. [x] **Add** Tailwind imports to `src/index.css` or `src/App.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
5. [x] **Start** dev server to confirm everything works:
   ```bash
   npm run dev
   ```
6. [x] **Optional**: Install additional packages (e.g., `axios`, `react-router-dom`, etc.):
   ```bash
   npm install react-router-dom axios
   ```

---

## 2. Global Setup (Layout, Router, Tailwind)

1. [x] **Create** a `src/router.tsx` or `src/Router.tsx` to define routes. Install React Router if not done:
   ```bash
   npm install react-router-dom
   ```
2. [x] **Set up** `<BrowserRouter>` in `main.tsx`:
   ```tsx
   import React from 'react'
   import ReactDOM from 'react-dom/client'
   import { BrowserRouter } from 'react-router-dom'
   import App from './App'
   import './index.css'

   ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
     <React.StrictMode>
       <BrowserRouter>
         <App />
       </BrowserRouter>
     </React.StrictMode>,
   )
   ```
3. [x] **In** `App.tsx`, define your routes:
   ```tsx
   import { Routes, Route } from 'react-router-dom'
   import DashboardPage from './pages/DashboardPage'
   import ActivitiesIndexPage from './pages/ActivitiesIndexPage'
   import ActivityShowPage from './pages/ActivityShowPage'
   import ActivityLaunchPage from './pages/ActivityLaunchPage'
   import WordsIndexPage from './pages/WordsIndexPage'
   import WordShowPage from './pages/WordShowPage'
   import GroupsIndexPage from './pages/GroupsIndexPage'
   import GroupShowPage from './pages/GroupShowPage'
   import StudySessionsIndexPage from './pages/StudySessionsIndexPage'
   import StudySessionShowPage from './pages/StudySessionShowPage'
   import SettingsPage from './pages/SettingsPage'

   function App() {
     return (
       <Routes>
         <Route path="/" element={<DashboardPage />} />
         <Route path="/dashboard" element={<DashboardPage />} />

         <Route path="/study_activities" element={<ActivitiesIndexPage />} />
         <Route path="/study_activities/:id" element={<ActivityShowPage />} />
         <Route path="/study_activities/:id/launch" element={<ActivityLaunchPage />} />

         <Route path="/words" element={<WordsIndexPage />} />
         <Route path="/words/:id" element={<WordShowPage />} />

         <Route path="/groups" element={<GroupsIndexPage />} />
         <Route path="/groups/:id" element={<GroupShowPage />} />

         <Route path="/study_sessions" element={<StudySessionsIndexPage />} />
         <Route path="/study_sessions/:id" element={<StudySessionShowPage />} />

         <Route path="/settings" element={<SettingsPage />} />
       </Routes>
     )
   }

   export default App
   ```
4. [x] **Create** a global layout (optional) for a navbar or sidebar:
   - Example: `src/components/Layout.tsx` with a header, sidebar, etc.

---

## 3. Dashboard Page (`/dashboard`)

**Purpose**: Provide a summary of learning and be the default page.

### Components

1. [x] **DashboardPage** (in `src/pages/DashboardPage.tsx`):
   - [x] **Layout**: Possibly wrap in a `<Layout>` if you created one.
   - [x] **Use** a custom hook or `axios` calls to fetch data from:
     - `GET /api/dashboard/last_study_session`
     - `GET /api/dashboard/study_progress`
     - `GET /api/dashboard/quick_stats`

2. [x] **Sections**:
   1. **Last Study Session**
      - [x] Render last session info: activity used, time, summary of correct vs wrong if available
      - [ ] Link to group or session details if possible
   2. **Study Progress**
      - [x] Show total words studied: e.g. `3 / 124`
      - [x] Show a mastery progress bar (0%).
   3. **Quick Stats**
      - [x] success rate (80%), total sessions, active groups, study streak days
   4. **Start Studying Button**
      - [x] Link to `/study_activities`

### Steps

1. [x] **Setup** `useEffect` or `react-query` to fetch the three endpoints in parallel or sequentially.
2. [x] **Store** the results in state (e.g. `const [lastSession, setLastSession] = useState(null)`, etc.).
3. [x] **Render** the data in Tailwind-based cards or sections.
4. [x] **Add** a button: `<Link to="/study_activities">Start Studying</Link>`.
5. [x] **Test** by visiting `/dashboard` in the browser.

---

## 4. Study Activities Index (`/study_activities`)

**Purpose**: Show a collection of study activities.

### Components

1. [x] **ActivitiesIndexPage** (in `src/pages/ActivitiesIndexPage.tsx`):
   - [x] **Fetch** data from `GET /api/study_activities`
     - This endpoint may or may not exist as a "list all activities." If needed, you might adjust to a custom endpoint or a static list.  
   - [x] **Render** a list of **ActivityCard** components.

2. [x] **ActivityCard** (in `src/components/ActivityCard.tsx`):
   - [x] Props:
     - `name`
     - `thumbnail_url`
     - (optional) `description` if needed
   - [x] **Layout** in Tailwind: an image, name, and two buttons:
     - **Launch** → goes to `"/study_activities/:id/launch"`
     - **View** → goes to `"/study_activities/:id"`

### Steps

1. [x] **Create** a small interface `IActivity` in TypeScript for type-checking:
   ```ts
   interface IActivity {
     id: number
     name: string
     thumbnail_url: string
     description: string
   }
   ```
2. [x] **Fetch** activities, store in state, map over them to render `<ActivityCard />`.
3. [x] **Test** the page by navigating to `/study_activities`.

---

## 5. Study Activity Show (`/study_activities/:id`)

**Purpose**: Show details of a single study activity and its past sessions.

### Components

1. [x] **ActivityShowPage** (in `src/pages/ActivityShowPage.tsx`):
   - [x] **Fetch** from `GET /api/study_activities/:id` for details:
     - name, thumbnail, description
   - [x] **Fetch** from `GET /api/study_activities/:id/study_sessions` for paginated list
2. [ ] **SessionsList** (in `src/components/SessionsList.tsx` maybe) to display:
   - `id`, `activity_name`, `group_name`, `start_time`, `end_time`, `review_items_count`
   - Paginated: handle `page` param if provided by the API.

### Steps

1. [x] **Get** the `id` from `useParams()`.
2. [x] **Fetch** activity details → store in state, render top portion with name, thumbnail, description.
3. [x] **Fetch** the sessions → store in state, render in a table or card list.
4. [x] **Implement** pagination logic (e.g., next/prev buttons).
5. [x] **Add** a button to **Launch** the activity (link to `/:id/launch`).

---

## 6. Study Activity Launch (`/study_activities/:id/launch`)

**Purpose**: Launch a study activity by **posting** a new session.

### Components

1. [x] **ActivityLaunchPage**:
   - [x] **Display** the activity name (from `GET /api/study_activities/:id` or pass from previous page).
   - [x] **Form**: `<select>` for group, `<button>` to launch
     - **Groups**: Fetch from `GET /api/groups` or similar to populate a dropdown.
   - [x] **On** form submit → call `POST /api/study_activities` with `group_id` and `study_activity_id`.
   - [x] On success: open a new tab with the returned URL (if that’s how your activity is launched externally), then redirect to the newly created study session’s page (the backend might return `id` of the new study session).

### Steps

1. [x] **Fetch** activity name for UI.
2. [x] **Fetch** group list for the select input.
3. [x] **Submit** form with `study_activity_id` (from route params) + selected `group_id`.
4. [x] **Handle** success → navigate to `/study_sessions/:newSessionId`.

---

## 7. Words Index (`/words`)

**Purpose**: Show all words in the database, **paginated**.

### Components

1. [x] **WordsIndexPage** (in `src/pages/WordsIndexPage.tsx`):
   - [x] **Fetch** from `GET /api/words?page=1&...`
   - [x] **Render** a table:
     - Jamaican Patois
     - English
     - Correct Count
     - Wrong Count
   - [x] **Pagination** controls
   - [x] Clicking Jamaican Patois → `"/words/:id"`

### Steps

1. [x] **Define** `IWord` interface:
   ```ts
   interface IWord {
     id: number
     jamaican_patois: string
     english: string
     correct_count: number
     wrong_count: number
   }
   ```
2. [x] **Fetch** `items` and `pagination` from the API response, store in state.
3. [x] **Map** over items to display in table rows.
4. [x] **Implement** next/prev page if `pagination` indicates more pages.

---

## 8. Word Show (`/words/:id`)

**Purpose**: Show info for a specific word.

### Components

1. [x] **WordShowPage** (in `src/pages/WordShowPage.tsx`):
   - [x] **Fetch** from `GET /api/words/:id`
   - [x] **Display** Jamaican Patois, English, stats (correct vs. wrong).
   - [x] **Render** group tags or pills: if user clicks, route to `"/groups/:groupId"`.

### Steps

1. [x] **Get** `id` from `useParams()`.
2. [x] **Fetch** word data, store in state: e.g., `const [word, setWord] = useState<WordType | null>(null)`.
3. [x] **Render** the details in a card or simple layout.
4. [x] **Test** by navigating to `/words/1` (assuming word 1 exists).

---

## 9. Word Groups Index (`/groups`)

**Purpose**: Show a list of groups in the database.

### Components

1. [x] **GroupsIndexPage** (in `src/pages/GroupsIndexPage.tsx`):
   - [x] **Fetch** from `GET /api/groups?page=1`
   - [x] **Render** table: (Group Name, Word Count)
   - [x] **Pagination** logic
   - [x] Clicking group name → `"/groups/:id"`

### Steps

1. [x] **Define** `IGroup` interface:
   ```ts
   interface IGroup {
     id: number
     name: string
     word_count: number
   }
   ```
2. [x] **Fetch** data, store, map to table rows.
3. [x] **Implement** next/prev for pagination if needed.

---

## 10. Group Show (`/groups/:id`)

**Purpose**: Show info about a specific group, including stats, words in the group, and study sessions.

### Components

1. [x] **GroupShowPage**:
   - [x] **Fetch** from `GET /api/groups/:id` → group name + stats (word count).
   - [x] **Words** in group (paginated):
     - from `GET /api/groups/:id/words`
     - Reuse `WordsList` or similar if you want a consistent table.
   - [x] **Study Sessions** for this group:
     - from `GET /api/groups/:id/study_sessions`
     - Reuse `SessionsList` to keep consistent UI.

### Steps

1. [x] **Get** `id` from `useParams()`.
2. [x] **Fetch** group details (name, stats).
3. [x] **Fetch** words in the group (paginated).
4. [x] **Fetch** sessions in the group (paginated).
5. [x] **Render** them in separate sections.

---

## 11. Study Sessions Index (`/study_sessions`)

**Purpose**: Show a list of all study sessions in the database.

### Components

1. [x] **StudySessionsIndexPage**:
   - [x] **Fetch** from `GET /api/study_sessions?page=1`
   - [x] Render columns: `id`, `activity name`, `group name`, `start time`, `end time`, `review items`.
   - [x] Pagination logic
   - [x] Click `id` → go to `"/study_sessions/:id"`

### Steps

1. [x] **Define** session interface.
2. [x] **Fetch** data, store, show table.
3. [x] **Handle** pagination.  
4. [x] **Test** by navigating to `/study_sessions`.

---

## 12. Study Session Show (`/study_sessions/:id`)

**Purpose**: Show details of a specific study session.

### Components

1. [x] **StudySessionShowPage**:
   - [x] **Fetch** from `GET /api/study_sessions/:id`
     - activity name, group name, start time, end time, review items count
   - [x] **Fetch** words from `GET /api/study_sessions/:id/words`
     - Possibly reusing a `WordsList` to display them in a paginated manner.

### Steps

1. [x] **Get** `id` from `useParams()`.
2. [x] **Fetch** session details → display top info.
3. [x] **Fetch** session words → display in table, with pagination as needed.
4. [x] **Test** by going to `"/study_sessions/1"`.

---

## 13. Settings Page (`/settings`)

**Purpose**: Manage configurations like theme and reset actions.

### Components

1. [ ] **SettingsPage**:
   - [ ] **Theme Selection**: (Light, Dark, System Default)  
     - Possibly store in local storage or global state.
   - [ ] **Reset History Button** → `POST /api/reset_history`
   - [ ] **Full Reset Button** → `POST /api/full_reset`
   - [ ] On success, show a toast or alert that the action completed.

### Steps

1. [ ] **Create** a `SettingsPage.tsx`.
2. [ ] **Implement** theme toggles (optional).
3. [ ] **Hook** up onClick for “Reset History” to call the endpoint:
   ```ts
   // example with fetch or axios
   await axios.post('/api/reset_history')
   alert('History reset!')
   ```
4. [ ] **Hook** up “Full Reset” similarly.
5. [ ] **Test** each button.

---

## 14. Testing and Final Review

1. [ ] **Review** each page, ensure the data is fetched from the correct endpoint, displayed properly, and navigations are correct.
2. [ ] **Test** pagination by switching pages on Words/Groups/Study Sessions, etc.
3. [ ] **Test** the “Start Studying” flow:
   - /dashboard → Start Studying → /study_activities → /study_activities/:id/launch → Create session → redirect to /study_sessions/:newId
4. [ ] **Verify** the settings page reset endpoints:
   - `POST /api/reset_history` → check if sessions and reviews are cleared
   - `POST /api/full_reset` → check if everything is wiped and re-seeded if that’s how the backend is set up.

---

# Conclusion

By following these **atomic steps**, a junior dev can **incrementally build** the React + TypeScript + Tailwind + Vite frontend:

1. **Initialize** the project with Vite + TS + Tailwind.  
2. **Set up** a global layout and routing with React Router.  
3. **Create** each page according to the **Front-End Technical Spec**.  
4. **Ensure** each component properly **fetches** data from the described **endpoints** and **renders** in a user-friendly manner.  
5. **Test** thoroughly, including pagination, navigation flows, and reset features.

This approach keeps the focus on **one page (or component) at a time**, ensuring a smooth development process. Good luck building the **Lang Portal** frontend!