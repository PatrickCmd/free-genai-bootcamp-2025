import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { LastStudySession, StudyProgress, QuickStats } from '../types/dashboard';
import LastSessionCard from '../components/dashboard/LastSessionCard';

const Dashboard: React.FC = () => {
  const [lastSession, setLastSession] = useState<LastStudySession | null>(null);
  const [studyProgress, setStudyProgress] = useState<StudyProgress | null>(null);
  const [quickStats, setQuickStats] = useState<QuickStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [
          lastSessionRes,
          studyProgressRes,
          quickStatsRes
        ] = await Promise.all([
          api.get<LastStudySession>('/dashboard/last_study_session'),
          api.get<StudyProgress>('/dashboard/study_progress'),
          api.get<QuickStats>('/dashboard/quick-stats')
        ]);

        setLastSession(lastSessionRes.data);
        setStudyProgress(studyProgressRes.data);
        setQuickStats(quickStatsRes.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <LastSessionCard session={lastSession} loading={loading} />
        
        {/* Study Progress Card */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Study Progress</h2>
          {loading ? (
            <div className="animate-pulse space-y-2">
              <div className="h-4 bg-gray-700 rounded w-1/2"></div>
              <div className="h-4 bg-gray-700 rounded w-3/4"></div>
            </div>
          ) : studyProgress && (
            <div className="space-y-2">
              <p>
                <span className="text-gray-400">Words Reviewed:</span>{' '}
                {studyProgress.total_words_reviewed}
              </p>
              <p>
                <span className="text-gray-400">Accuracy Rate:</span>{' '}
                {studyProgress.accuracy_rate.toFixed(1)}%
              </p>
              <div className="mt-4">
                <div className="bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-blue-600 rounded-full h-2"
                    style={{ width: `${studyProgress.accuracy_rate}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Quick Stats Card */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
          {loading ? (
            <div className="animate-pulse space-y-2">
              <div className="h-4 bg-gray-700 rounded w-1/2"></div>
              <div className="h-4 bg-gray-700 rounded w-3/4"></div>
            </div>
          ) : quickStats && (
            <div className="space-y-2">
              <p>
                <span className="text-gray-400">Success Rate:</span>{' '}
                {quickStats.recent_accuracy.toFixed(1)}%
              </p>
              <p>
                <span className="text-gray-400">Words Learned:</span>{' '}
                {quickStats.words_learned} / {quickStats.total_words}
              </p>
              <p>
                <span className="text-gray-400">Study Streak:</span>{' '}
                {quickStats.streak_days} days
              </p>
              <p>
                <span className="text-gray-400">Total Study Time:</span>{' '}
                {quickStats.total_study_time_minutes} minutes
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 