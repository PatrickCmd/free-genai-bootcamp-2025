import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Word } from '../types/words';

interface PaginatedResponse {
  words: Word[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
}

const WordsIndex: React.FC = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchWords = async () => {
      try {
        const response = await api.get<PaginatedResponse>(`/words?page=${currentPage}&page_size=10`);
        setWords(response.data.words);
        setTotalPages(response.data.pagination.total_pages);
      } catch (err) {
        console.error('Error fetching words:', err);
        setError('Failed to load words');
      } finally {
        setLoading(false);
      }
    };

    fetchWords();
  }, [currentPage]);

  if (loading) {
    return (
      <div className="space-y-4">
        <h1 className="text-3xl font-bold">Words</h1>
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
      <h1 className="text-3xl font-bold">Words</h1>

      {/* Words Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-800">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold">Jamaican Patois</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">English</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
              <th className="px-6 py-3 text-right text-sm font-semibold">Correct</th>
              <th className="px-6 py-3 text-right text-sm font-semibold">Wrong</th>
              <th className="px-6 py-3 text-right text-sm font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {words.map(word => (
              <tr key={word.id} className="hover:bg-gray-800">
                <td className="px-6 py-4">
                  <Link 
                    to={`/words/${word.id}`}
                    className="text-blue-400 hover:text-blue-300"
                  >
                    {word.jamaican_patois}
                  </Link>
                </td>
                <td className="px-6 py-4">{word.english}</td>
                <td className="px-6 py-4">{word.parts?.type || '-'}</td>
                <td className="px-6 py-4 text-right text-green-500">{word.correct_count}</td>
                <td className="px-6 py-4 text-right text-red-500">{word.wrong_count}</td>
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
    </div>
  );
};

export default WordsIndex; 