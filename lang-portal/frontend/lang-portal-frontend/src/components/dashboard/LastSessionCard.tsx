import React from 'react';
import { Link } from 'react-router-dom';
import { LastStudySession } from '../../types/dashboard';
import { ClockIcon } from '@heroicons/react/24/outline';

interface Props {
  session: LastStudySession | null;
  loading: boolean;
}

const LastSessionCard: React.FC<Props> = ({ session, loading }) => {
  if (loading) {
    return (
      <div className="bg-gray-800 rounded-lg p-6 animate-pulse">
        <div className="h-4 bg-gray-700 rounded w-1/4 mb-4"></div>
        <div className="h-4 bg-gray-700 rounded w-3/4"></div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <ClockIcon className="w-6 h-6" />
          Last Study Session
        </h2>
        <p className="text-gray-400">No sessions yet</p>
        <Link 
          to="/study_activities" 
          className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Start your first session
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <ClockIcon className="w-6 h-6" />
        Last Study Session
      </h2>
      <div className="space-y-2">
        <p><span className="text-gray-400">Activity:</span> {session.activity_name}</p>
        <p><span className="text-gray-400">Group:</span> {session.group_name}</p>
        <p><span className="text-gray-400">Words Reviewed:</span> {session.review_items_count}</p>
        <p>
          <span className="text-gray-400">When:</span>{' '}
          {new Date(session.start_time).toLocaleString()}
        </p>
      </div>
      <div className="mt-4 space-x-4">
        <Link 
          to={`/study_sessions/${session.id}`}
          className="text-blue-400 hover:text-blue-300"
        >
          View Details
        </Link>
        <Link 
          to={`/study_activities`}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Start New Session
        </Link>
      </div>
    </div>
  );
};

export default LastSessionCard; 