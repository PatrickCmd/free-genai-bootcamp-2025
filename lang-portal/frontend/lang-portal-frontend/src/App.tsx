import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';

// Placeholder components until we implement them
const DashboardPage = () => <div className="text-center text-2xl">Dashboard Page</div>;
const StudyActivitiesIndex = () => <div className="text-center text-2xl">Study Activities Page</div>;
const StudyActivityShow = () => <div className="text-center text-2xl">Study Activity Show Page</div>;
const StudyActivityLaunch = () => <div className="text-center text-2xl">Study Activity Launch Page</div>;
const WordsIndex = () => <div className="text-center text-2xl">Words Index Page</div>;
const WordShow = () => <div className="text-center text-2xl">Word Show Page</div>;
const GroupsIndex = () => <div className="text-center text-2xl">Groups Index Page</div>;
const GroupShow = () => <div className="text-center text-2xl">Group Show Page</div>;
const StudySessionsIndex = () => <div className="text-center text-2xl">Study Sessions Index Page</div>;
const StudySessionShow = () => <div className="text-center text-2xl">Study Session Show Page</div>;
const Settings = () => <div className="text-center text-2xl">Settings Page</div>;

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        
        <Route path="/study_activities" element={<StudyActivitiesIndex />} />
        <Route path="/study_activities/:id" element={<StudyActivityShow />} />
        <Route path="/study_activities/:id/launch" element={<StudyActivityLaunch />} />
        
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
