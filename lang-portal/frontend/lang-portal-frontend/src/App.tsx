import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import StudyActivitiesIndex from './pages/StudyActivitiesIndex';
import StudyActivityShow from './pages/StudyActivityShow';
import StudyActivityLaunch from './pages/StudyActivityLaunch';
import WordsIndex from './pages/WordsIndex';
import WordShow from './pages/WordShow';
import StudyActivityCreate from './pages/StudyActivityCreate';
import GroupsIndex from './pages/GroupsIndex';
import GroupShow from './pages/GroupShow';
import StudySessionsIndex from './pages/StudySessionsIndex';
import StudySessionShow from './pages/StudySessionShow';
import Settings from './pages/Settings';

// Placeholder components until we implement them
const DashboardPage = () => <div className="text-center text-2xl">Dashboard Page</div>;

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        
        <Route path="/study_activities" element={<StudyActivitiesIndex />} />
        <Route path="/study_activities/:id" element={<StudyActivityShow />} />
        <Route path="/study_activities/:id/launch" element={<StudyActivityLaunch />} />
        <Route path="/study_activities/new" element={<StudyActivityCreate />} />
        
        <Route path="/words" element={<WordsIndex />} />
        <Route path="/words/:id" element={<WordShow />} />
        
        <Route path="/groups" element={<GroupsIndex />} />
        <Route path="/groups/:id" element={<GroupShow />} />
        
        <Route path="/study_sessions" element={<StudySessionsIndex />} />
        <Route path="/study_sessions/:id" element={<StudySessionShow />} />
        
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  );
}

export default App;
