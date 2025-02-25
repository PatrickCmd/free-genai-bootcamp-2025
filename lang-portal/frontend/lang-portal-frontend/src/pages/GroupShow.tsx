import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { Group } from '../types/groups';
import { Word, PaginatedWords } from '../types/words';
import { StudySession, PaginatedSessions } from '../types/studySessions';

const GroupShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [group, setGroup] = useState<Group | null>(null);
  const [words, setWords] = useState<Word[]>([]);
  const [sessions, setSessions] = useState<StudySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentWordsPage, setCurrentWordsPage] = useState(1);
  const [totalWordsPages, setTotalWordsPages] = useState(1);
  const [currentSessionsPage, setCurrentSessionsPage] = useState(1);
  const [totalSessionsPages, setTotalSessionsPages] = useState(1);

  useEffect(() => {
    const fetchGroupData = async () => {
      try {
        const [groupRes, wordsRes, sessionsRes] = await Promise.all([
          api.get<Group>(`/groups/${id}`),
          api.get<PaginatedWords>(`/groups/${id}/words?page=${currentWordsPage}`),
          api.get<PaginatedSessions>(`/groups/${id}/study_sessions?page=${currentSessionsPage}`)
        ]);

        setGroup(groupRes.data);
        setWords(wordsRes.data.words);
        setTotalWordsPages(wordsRes.data.pagination.total_pages);
        setSessions(sessionsRes.data.study_sessions);
        setTotalSessionsPages(sessionsRes.data.pagination.total_pages);
      } catch (err) {
        console.error('Error fetching group data:', err);
        setError('Failed to load group details');
      } finally {
        setLoading(false);
      }
    };

    fetchGroupData();
  }, [id, currentWordsPage, currentSessionsPage]);

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

  if (error || !group) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error || 'Group not found'}</p>
        <Link 
          to="/groups"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Groups
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Group Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">{group.name}</h1>
            {group.description && (
              <p className="text-gray-400">{group.description}</p>
            )}
          </div>
          <Link
            to={`/study_activities/new?group=${group.id}`}
            className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Study Group
          </Link>
        </div>
        <p className="text-gray-400">
          Total Words: {group.word_count}
        </p>
      </div>

      {/* Words Section */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Words</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-800">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold">Jamaican Patois</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">English</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
                <th className="px-6 py-3 text-right text-sm font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {words.map(word => (
                <tr key={word.id} className="hover:bg-gray-800">
                  <td className="px-6 py-4">{word.jamaican_patois}</td>
                  <td className="px-6 py-4">{word.english}</td>
                  <td className="px-6 py-4">{word.parts?.type || '-'}</td>
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

        {/* Words Pagination */}
        <div className="flex justify-center items-center space-x-4">
          <button
            onClick={() => setCurrentWordsPage(p => Math.max(1, p - 1))}
            disabled={currentWordsPage === 1}
            className={`px-4 py-2 rounded ${
              currentWordsPage === 1
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Previous
          </button>
          <span className="text-gray-400">
            Page {currentWordsPage} of {totalWordsPages}
          </span>
          <button
            onClick={() => setCurrentWordsPage(p => Math.min(totalWordsPages, p + 1))}
            disabled={currentWordsPage === totalWordsPages}
            className={`px-4 py-2 rounded ${
              currentWordsPage === totalWordsPages
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Next
          </button>
        </div>
      </div>

      {/* Study Sessions Section */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Study Sessions</h2>
        <div className="grid gap-4">
          {sessions.map(session => (
            <div key={session.id} className="bg-gray-800 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-lg font-semibold">
                    {session.activity_name}
                  </p>
                  <p className="text-gray-400">
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

        {/* Sessions Pagination */}
        <div className="flex justify-center items-center space-x-4">
          <button
            onClick={() => setCurrentSessionsPage(p => Math.max(1, p - 1))}
            disabled={currentSessionsPage === 1}
            className={`px-4 py-2 rounded ${
              currentSessionsPage === 1
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Previous
          </button>
          <span className="text-gray-400">
            Page {currentSessionsPage} of {totalSessionsPages}
          </span>
          <button
            onClick={() => setCurrentSessionsPage(p => Math.min(totalSessionsPages, p + 1))}
            disabled={currentSessionsPage === totalSessionsPages}
            className={`px-4 py-2 rounded ${
              currentSessionsPage === totalSessionsPages
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

export default GroupShow; 