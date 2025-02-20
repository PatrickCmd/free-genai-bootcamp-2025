# Lang Portal Frontend

Frontend application for the Language Learning Portal built with React, TypeScript, Tailwind CSS, and Vite.

## Project Setup Progress

### 1. Project Initialization ✅

- [x] Create new Vite + React + TypeScript project
- [x] Install Tailwind CSS
- [x] Configure Tailwind CSS
- [x] Add Tailwind directives
- [x] Verify setup works
- [x] Install additional packages

### 2. Global Setup (Layout, Router, Tailwind) ✅

- [x] Set up BrowserRouter in main.tsx
- [x] Define routes in App.tsx
- [x] Create global Layout component
- [x] Create common components (Header, Footer)

### 3. Dashboard Page (`/dashboard`) ✅

- [x] Set up API service
- [x] Create dashboard types
- [x] Implement LastSessionCard component
- [x] Create Dashboard page with:
  - Last Study Session
  - Study Progress
  - Quick Stats
- [x] Add loading states
- [x] Style with Tailwind CSS

### 4. Study Activities Index (`/study_activities`) ⏳
### 5. Study Activity Show (`/study_activities/:id`) 🔄
### 6. Study Activity Launch (`/study_activities/:id/launch`) 🔄
### 7. Words Index (`/words`) 🔄
### 8. Word Show (`/words/:id`) 🔄
### 9. Word Groups Index (`/groups`) 🔄
### 10. Group Show (`/groups/:id`) 🔄
### 11. Study Sessions Index (`/study_sessions`) 🔄
### 12. Study Session Show (`/study_sessions/:id`) 🔄
### 13. Settings Page (`/settings`) 🔄
### 14. Testing and Final Review 🔄

## Setup Steps Completed

1. Created new Vite project with React and TypeScript
2. Installed Tailwind CSS v4 and its dependencies:
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```
3. Configured Vite for Tailwind CSS:
   - Updated vite.config.ts to include Tailwind plugin
   - Added Tailwind import to src/index.css
4. Installed additional required packages:
   ```bash
   npm install react-router-dom axios
   ```
5. Setting up Global Layout and Routing:
   - Created Layout component with Header and Footer
   - Configured BrowserRouter in main.tsx
   - Set up route structure in App.tsx
   - Created placeholder components for all pages
6. Implemented Dashboard Page:
   - Created API service for backend communication
   - Added TypeScript interfaces for type safety
   - Built responsive dashboard layout with 3 main cards
   - Implemented loading states and error handling
   - Added navigation to other sections

## Dashboard Implementation

The dashboard consists of three main components:

![Dashboard Page](./screenshots/dashboard.png)

### Last Study Session Card
Shows information about the most recent study session including:
- Activity name
- Group name
- Number of words reviewed
- Session timestamp
- Links to view details or start a new session


### Study Progress Card
Displays overall study progress including:
- Total words reviewed
- Accuracy rate with progress bar
- Words by group statistics


### Quick Stats Card
Shows key statistics including:
- Success rate
- Words learned vs total words
- Study streak
- Total study time


## Development

To start the development server:

```bash
npm run dev
```

## Building

To create a production build:

```bash
npm run build
```

## API Integration

The frontend communicates with the backend API at `http://127.0.0.1:8000/api` using the following endpoints:

- `GET /dashboard/last_study_session`
- `GET /dashboard/study_progress`
- `GET /dashboard/quick-stats`

## Component Structure

```
src/
├── components/
│   ├── dashboard/
│   │   └── LastSessionCard.tsx
│   ├── Layout.tsx
│   ├── Header.tsx
│   └── Sidebar.tsx
├── pages/
│   └── Dashboard.tsx
├── services/
│   └── api.ts
└── types/
    └── dashboard.ts
``` 