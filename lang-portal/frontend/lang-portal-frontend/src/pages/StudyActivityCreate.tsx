import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../services/api';
import { StudyActivity } from '../types/studyActivities';
import { Word } from '../types/words';
import { Group } from '../types/groups';

const StudyActivityCreate: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [word, setWord] = useState<Word | null>(null);
  const [group, setGroup] = useState<Group | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const wordId = searchParams.get('word');
  const groupId = searchParams.get('group');

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (wordId) {
          // Fetch word details and its groups
          const wordResponse = await api.get<Word>(`/words/${wordId}`);
          const groupResponse = await api.get<{ groups: Group[] }>(`/words/${wordId}/groups`);
          setWord(wordResponse.data);
          if (groupResponse.data.groups.length > 0) {
            setGroup(groupResponse.data.groups[0]);
          }
        } else if (groupId) {
          // Fetch group details
          const groupResponse = await api.get<Group>(`/groups/${groupId}`);
          setGroup(groupResponse.data);
        } else {
          setError('No word or group specified');
        }
      } catch (err) {
        console.error('Error fetching details:', err);
        setError('Failed to load details');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [wordId, groupId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!group) return;

    try {
      const response = await api.post<StudyActivity>('/study_activities', {
        name: word 
          ? `Review: ${word.jamaican_patois}`
          : `Study: ${group.name}`,
        group_id: group.id
      });

      // Navigate to the launch page of the new activity
      navigate(`/study_activities/${response.data.id}/launch`);
    } catch (err) {
      console.error('Error creating study activity:', err);
      setError('Failed to create study activity');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || (!word && !group)) {
    return (
      <div className="text-center">
        <p className="text-red-500 mb-4">{error || 'No details found'}</p>
        <button
          onClick={() => navigate(-1)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create Study Activity</h1>
      
      <div className="bg-gray-800 rounded-lg p-6">
        {/* Details Section */}
        <div className="mb-6 pb-6 border-b border-gray-700">
          {word ? (
            <>
              <h2 className="text-2xl font-bold mb-2">{word.jamaican_patois}</h2>
              <p className="text-gray-400">{word.english}</p>
              {word.parts && (
                <p className="text-sm text-gray-500 mt-2">
                  Type: {word.parts.type}, Usage: {word.parts.usage}
                </p>
              )}
            </>
          ) : group && (
            <>
              <h2 className="text-2xl font-bold mb-2">{group.name}</h2>
              {group.description && (
                <p className="text-gray-400">{group.description}</p>
              )}
              <p className="text-sm text-gray-500 mt-2">
                Words: {group.word_count}
              </p>
            </>
          )}
        </div>

        {/* Actions */}
        <div className="flex justify-between">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="text-gray-400 hover:text-gray-300"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Create & Launch
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudyActivityCreate; 