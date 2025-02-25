import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { StudySession, PaginatedSessions } from '../types/studySessions';

const StudySessionsIndex: React.FC = () => {
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await api.get<PaginatedSessions>(`/study_sessions?page=${currentPage}&page_size=10`);
        setSessions(response.data.study_sessions);
        setTotalPages(response.data.pagination.total_pages);
      } catch (err) {
        console.error('Error fetching study sessions:', err);
        setError('Failed to load study sessions');
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, [currentPage]);

  if (loading) {
    return (
      <div className="space-y-4">
        <h1 className="text-3xl font-bold">Study Sessions</h1>
        <div className="animate-pulse">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="bg-gray-800 p-4 rounded-lg mb-2">
              <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-700 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error}</p>
        <button 
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Study Sessions</h1>

      {/* Sessions List */}
      <div className="space-y-4">
        {sessions.map(session => (
          <div key={session.id} className="bg-gray-800 rounded-lg p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-semibold mb-2">
                  {session.activity_name}
                </h2>
                <p className="text-gray-400">
                  Group: {session.group_name}
                </p>
                <p className="text-gray-400">
                  Started: {new Date(session.start_time).toLocaleString()}
                </p>
                <p className="text-gray-400">
                  Words Reviewed: {session.review_items_count}
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  to={`/study_sessions/${session.id}`}
                  className="text-blue-400 hover:text-blue-300"
                >
                  View Details
                </Link>
                {!session.end_time && (
                  <Link
                    to={`/study_activities/${session.id}/launch`}
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                  >
                    Continue Session
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}

        {sessions.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 mb-4">No study sessions found</p>
            <Link 
              to="/study_activities/new"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Start Your First Session
            </Link>
          </div>
        )}
      </div>

      {/* Pagination Controls */}
      {sessions.length > 0 && (
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
      )}
    </div>
  );
};

export default StudySessionsIndex; 