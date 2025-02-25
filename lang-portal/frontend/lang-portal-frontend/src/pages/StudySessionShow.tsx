import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { StudySession } from '../types/studySessions';
import { Word, PaginatedWords } from '../types/words';

const StudySessionShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [session, setSession] = useState<StudySession | null>(null);
  const [words, setWords] = useState<Word[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchSessionData = async () => {
      try {
        const [sessionRes, wordsRes] = await Promise.all([
          api.get<StudySession>(`/study_sessions/${id}`),
          api.get<PaginatedWords>(`/study_sessions/${id}/words?page=${currentPage}`)
        ]);

        setSession(sessionRes.data);
        setWords(wordsRes.data.words);
        setTotalPages(wordsRes.data.pagination.total_pages);
      } catch (err) {
        console.error('Error fetching session data:', err);
        setError('Failed to load session details');
      } finally {
        setLoading(false);
      }
    };

    fetchSessionData();
  }, [id, currentPage]);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-gray-800 rounded-lg p-6 animate-pulse">
          <div className="h-8 bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error || 'Session not found'}</p>
        <Link 
          to="/study_sessions"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Sessions
        </Link>
      </div>
    );
  }

  // Calculate session duration if ended
  const duration = session.end_time
    ? Math.round((new Date(session.end_time).getTime() - new Date(session.start_time).getTime()) / 60000)
    : null;

  return (
    <div className="space-y-6">
      {/* Session Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">{session.activity_name}</h1>
            <p className="text-gray-400">Group: {session.group_name}</p>
          </div>
          {!session.end_time && (
            <Link
              to={`/study_activities/${session.id}/launch`}
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
            >
              Continue Session
            </Link>
          )}
        </div>

        {/* Session Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-gray-700 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Words Reviewed</h3>
            <p className="text-2xl">{session.review_items_count}</p>
          </div>
          
          <div className="bg-gray-700 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Started</h3>
            <p className="text-lg">{new Date(session.start_time).toLocaleString()}</p>
          </div>
          
          <div className="bg-gray-700 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">
              {session.end_time ? 'Duration' : 'Status'}
            </h3>
            <p className="text-lg">
              {session.end_time 
                ? `${duration} minutes`
                : 'In Progress'
              }
            </p>
          </div>
        </div>
      </div>

      {/* Words Section */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Reviewed Words</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold">Jamaican Patois</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">English</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
                <th className="px-6 py-3 text-center text-sm font-semibold">Result</th>
                <th className="px-6 py-3 text-right text-sm font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {words.map(word => (
                <tr key={word.id} className="hover:bg-gray-800">
                  <td className="px-6 py-4">{word.jamaican_patois}</td>
                  <td className="px-6 py-4">{word.english}</td>
                  <td className="px-6 py-4">{word.parts?.type || '-'}</td>
                  <td className="px-6 py-4 text-center">
                    <span className={`px-2 py-1 rounded ${
                      word.correct_count > word.wrong_count
                        ? 'bg-green-900 text-green-300'
                        : 'bg-red-900 text-red-300'
                    }`}>
                      {word.correct_count > word.wrong_count ? 'Correct' : 'Incorrect'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link 
                      to={`/words/${word.id}`}
                      className="text-blue-400 hover:text-blue-300"
                    >
                      View Details
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        <div className="flex justify-center items-center space-x-4">
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
      </div>
    </div>
  );
};

export default StudySessionShow; 