import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LearningPreferences } from '../types/settings';
import { getSettings, updateSettings } from '../services/settings';

interface LearningPreferences {
  wordsPerSession: number;
  reviewInterval: number;
  showPhonetics: boolean;
  showUsageExamples: boolean;
  darkMode: boolean;
}

const Settings: React.FC = () => {
  const navigate = useNavigate();
  const [preferences, setPreferences] = useState<LearningPreferences>({
    wordsPerSession: 10,
    reviewInterval: 24,
    showPhonetics: true,
    showUsageExamples: true,
    darkMode: true
  });
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const settings = await getSettings();
        setPreferences(settings);
      } catch (err) {
        console.error('Error fetching settings:', err);
        setError('Failed to load settings');
      }
    };

    fetchSettings();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setPreferences(prev => ({
      ...prev,
      [name]: type === 'checkbox' 
        ? (e.target as HTMLInputElement).checked 
        : type === 'number' 
          ? parseInt(value) 
          : value
    }));
    setSaved(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateSettings(preferences);
      setSaved(true);
      setError(null);
    } catch (err) {
      console.error('Error saving settings:', err);
      setError('Failed to save settings');
    }
  };

  const handleReset = () => {
    setPreferences({
      wordsPerSession: 10,
      reviewInterval: 24,
      showPhonetics: true,
      showUsageExamples: true,
      darkMode: true
    });
    setSaved(false);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Settings</h1>
        {saved && (
          <span className="text-green-500">
            Settings saved successfully
          </span>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Study Preferences Section */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Study Preferences</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Words per Study Session
              </label>
              <input
                type="number"
                name="wordsPerSession"
                min="1"
                max="50"
                value={preferences.wordsPerSession}
                onChange={handleChange}
                className="bg-gray-700 rounded px-3 py-2 w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Review Interval (hours)
              </label>
              <select
                name="reviewInterval"
                value={preferences.reviewInterval}
                onChange={handleChange}
                className="bg-gray-700 rounded px-3 py-2 w-full"
              >
                <option value="12">12 hours</option>
                <option value="24">24 hours</option>
                <option value="48">48 hours</option>
                <option value="72">72 hours</option>
              </select>
            </div>
          </div>
        </div>

        {/* Display Preferences Section */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Display Preferences</h2>
          
          <div className="space-y-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="showPhonetics"
                name="showPhonetics"
                checked={preferences.showPhonetics}
                onChange={handleChange}
                className="h-4 w-4 rounded border-gray-300"
              />
              <label htmlFor="showPhonetics" className="ml-2 block text-sm">
                Show phonetic pronunciation
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="showUsageExamples"
                name="showUsageExamples"
                checked={preferences.showUsageExamples}
                onChange={handleChange}
                className="h-4 w-4 rounded border-gray-300"
              />
              <label htmlFor="showUsageExamples" className="ml-2 block text-sm">
                Show usage examples
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="darkMode"
                name="darkMode"
                checked={preferences.darkMode}
                onChange={handleChange}
                className="h-4 w-4 rounded border-gray-300"
              />
              <label htmlFor="darkMode" className="ml-2 block text-sm">
                Dark mode
              </label>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-between items-center pt-4">
          <button
            type="button"
            onClick={handleReset}
            className="text-gray-400 hover:text-gray-300"
          >
            Reset to Defaults
          </button>

          <div className="space-x-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="text-gray-400 hover:text-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
            >
              Save Changes
            </button>
          </div>
        </div>

        {error && (
          <p className="text-red-500 text-center mt-4">{error}</p>
        )}
      </form>
    </div>
  );
};

export default Settings; 