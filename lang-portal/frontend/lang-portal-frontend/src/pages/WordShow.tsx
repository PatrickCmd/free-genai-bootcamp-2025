import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { Word } from '../types/words';

const WordShow: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [word, setWord] = useState<Word | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWord = async () => {
      try {
        const response = await api.get<Word>(`/words/${id}`);
        setWord(response.data);
      } catch (err) {
        console.error('Error fetching word:', err);
        setError('Failed to load word details');
      } finally {
        setLoading(false);
      }
    };

    fetchWord();
  }, [id]);

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="bg-gray-800 rounded-lg p-6 animate-pulse">
          <div className="h-8 bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (error || !word) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error || 'Word not found'}</p>
        <Link 
          to="/words"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Words
        </Link>
      </div>
    );
  }

  const accuracy = word.correct_count + word.wrong_count > 0
    ? (word.correct_count / (word.correct_count + word.wrong_count) * 100).toFixed(1)
    : 0;

  return (
    <div className="space-y-6">
      {/* Word Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="mb-4">
          <h1 className="text-3xl font-bold mb-2">{word.jamaican_patois}</h1>
          <p className="text-xl text-gray-400">{word.english}</p>
        </div>
        
        {word.parts && (
          <div className="mt-4 space-y-2">
            <p>
              <span className="text-gray-400">Type:</span>{' '}
              <span className="capitalize">{word.parts.type}</span>
            </p>
            <p>
              <span className="text-gray-400">Usage:</span>{' '}
              <span className="capitalize">{word.parts.usage}</span>
            </p>
          </div>
        )}
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Correct Reviews</h3>
          <p className="text-2xl text-green-500">{word.correct_count}</p>
        </div>
        
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Wrong Reviews</h3>
          <p className="text-2xl text-red-500">{word.wrong_count}</p>
        </div>
        
        <div className="bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-2">Accuracy Rate</h3>
          <p className="text-2xl text-blue-500">{accuracy}%</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Review Progress</h3>
        <div className="bg-gray-700 rounded-full h-4">
          <div 
            className="bg-blue-600 rounded-full h-4 transition-all duration-300"
            style={{ width: `${accuracy}%` }}
          ></div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <Link 
          to="/words"
          className="text-blue-400 hover:text-blue-300"
        >
          ← Back to Words
        </Link>
        <Link 
          to={`/study_activities/new?word=${word.id}`}
          className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
        >
          Study This Word
        </Link>
      </div>
    </div>
  );
};

export default WordShow; 