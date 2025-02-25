import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { StudyActivity } from '../types/studyActivities';
import { StudySession } from '../types/studySessions';

interface PaginatedSessions {
  study_sessions: StudySession[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}

const StudyActivityShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activity, setActivity] = useState<StudyActivity | null>(null);
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchActivityData = async () => {
      try {
        const [activityRes, sessionsRes] = await Promise.all([
          api.get<StudyActivity>(`/study_activities/${id}`),
          api.get<PaginatedSessions>(`/study_activities/${id}/study_sessions?page=${currentPage}`)
        ]);

        setActivity(activityRes.data);
        setSessions(sessionsRes.data.study_sessions);
        setTotalPages(sessionsRes.data.pagination.total_pages);
      } catch (err) {
        console.error('Error fetching activity data:', err);
        setError('Failed to load activity details');
      } finally {
        setLoading(false);
      }
    };

    fetchActivityData();
  }, [id, currentPage]);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-gray-800 rounded-lg p-6 animate-pulse">
          <div className="h-8 bg-gray-700 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gray-700 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (error || !activity) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error || 'Activity not found'}</p>
        <Link 
          to="/study_activities"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Activities
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Activity Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">{activity.name}</h1>
            <p className="text-gray-400">Group: {activity.group_name}</p>
          </div>
          <Link
            to={`/study_activities/${activity.id}/launch`}
            className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Launch Activity
          </Link>
        </div>
        <div className="mt-4">
          <p className="text-gray-400">
            Total Reviews: {activity.review_items_count}
          </p>
          <p className="text-gray-400">
            Created: {new Date(activity.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      {/* Study Sessions */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Study Sessions</h2>
        
        {sessions.length === 0 ? (
          <p className="text-gray-400">No study sessions yet.</p>
        ) : (
          <>
            <div className="grid gap-4">
              {sessions.map(session => (
                <div key={session.id} className="bg-gray-800 rounded-lg p-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-lg font-semibold">
                        {new Date(session.start_time).toLocaleString()}
                      </p>
                      <p className="text-gray-400">
                        Reviews: {session.review_items_count}
                      </p>
                    </div>
                    <Link
                      to={`/study_sessions/${session.id}`}
                      className="text-blue-400 hover:text-blue-300"
                    >
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination Controls */}
            <div className="flex justify-center items-center space-x-4 mt-6">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className={`px-4 py-2 rounded ${
                  currentPage === 1
                    ? 'bg-gray-600 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                Previous
              </button>
              <span className="text-gray-400">
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className={`px-4 py-2 rounded ${
                  currentPage === totalPages
                    ? 'bg-gray-600 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default StudyActivityShow; 