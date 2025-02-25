import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { StudyActivity } from '../types/studyActivities';
import { Word } from '../types/words';

interface ReviewWord extends Word {
  isReviewed: boolean;
  isCorrect?: boolean;
}

const StudyActivityLaunch: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activity, setActivity] = useState<StudyActivity | null>(null);
  const [words, setWords] = useState<ReviewWord[]>([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);

  useEffect(() => {
    const fetchActivityData = async () => {
      try {
        const [activityRes, wordsRes] = await Promise.all([
          api.get<StudyActivity>(`/study_activities/${id}`),
          api.get<{ words: Word[] }>(`/study_activities/${id}/words`)
        ]);

        setActivity(activityRes.data);
        setWords(wordsRes.data.words.map(word => ({ ...word, isReviewed: false })));
      } catch (err) {
        console.error('Error fetching activity data:', err);
        setError('Failed to load activity');
      } finally {
        setLoading(false);
      }
    };

    fetchActivityData();
  }, [id]);

  const handleReview = async (isCorrect: boolean) => {
    if (!activity || !words[currentWordIndex]) return;

    try {
      await api.post(`/study_sessions/${activity.study_session_id}/words/${words[currentWordIndex].id}/review`, {
        correct: isCorrect
      });

      setWords(prev => prev.map((word, idx) => 
        idx === currentWordIndex 
          ? { ...word, isReviewed: true, isCorrect }
          : word
      ));

      setShowAnswer(false);
      if (currentWordIndex < words.length - 1) {
        setCurrentWordIndex(prev => prev + 1);
      } else {
        // Activity completed
        navigate(`/study_sessions/${activity.study_session_id}`);
      }
    } catch (err) {
      console.error('Error submitting review:', err);
      setError('Failed to submit review');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !activity || !words.length) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500 mb-4">{error || 'No words available for review'}</p>
        <button
          onClick={() => navigate('/study_activities')}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Back to Activities
        </button>
      </div>
    );
  }

  const currentWord = words[currentWordIndex];
  const progress = ((currentWordIndex + 1) / words.length) * 100;

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="bg-gray-700 rounded-full h-2">
          <div 
            className="bg-blue-600 rounded-full h-2 transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <p className="text-gray-400 text-center mt-2">
          {currentWordIndex + 1} of {words.length} words
        </p>
      </div>

      {/* Word Card */}
      <div className="bg-gray-800 rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold mb-4">{currentWord.jamaican_patois}</h2>
        
        {showAnswer ? (
          <>
            <p className="text-xl text-gray-300 mb-8">{currentWord.english}</p>
            <div className="flex justify-center gap-4">
              <button
                onClick={() => handleReview(false)}
                className="bg-red-600 text-white px-8 py-3 rounded-lg hover:bg-red-700"
              >
                Incorrect
              </button>
              <button
                onClick={() => handleReview(true)}
                className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700"
              >
                Correct
              </button>
            </div>
          </>
        ) : (
          <button
            onClick={() => setShowAnswer(true)}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700"
          >
            Show Answer
          </button>
        )}
      </div>

      {/* Stats */}
      <div className="mt-8 grid grid-cols-2 gap-4">
        <div className="bg-gray-800 rounded-lg p-4 text-center">
          <p className="text-gray-400">Correct</p>
          <p className="text-2xl font-bold text-green-500">
            {words.filter(w => w.isReviewed && w.isCorrect).length}
          </p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4 text-center">
          <p className="text-gray-400">Incorrect</p>
          <p className="text-2xl font-bold text-red-500">
            {words.filter(w => w.isReviewed && !w.isCorrect).length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default StudyActivityLaunch; 