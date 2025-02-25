import api from './api';
import { LearningPreferences } from '../types/settings';

export const getSettings = async (): Promise<LearningPreferences> => {
  const response = await api.get<LearningPreferences>('/settings');
  return response.data;
};

export const updateSettings = async (preferences: LearningPreferences): Promise<LearningPreferences> => {
  const response = await api.post<LearningPreferences>('/settings', preferences);
  return response.data;
}; 