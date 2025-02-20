export interface LastStudySession {
  id: number;
  activity_name: string;
  group_name: string;
  start_time: string;
  end_time: string | null;
  review_items_count: number;
}

export interface StudyProgress {
  total_words_reviewed: number;
  total_correct: number;
  total_incorrect: number;
  accuracy_rate: number;
  total_study_sessions: number;
  total_study_time_minutes: number;
  words_by_group: Array<{
    group_id: number;
    group_name: string;
    unique_words: number;
    total_reviews: number;
    correct_reviews: number;
    accuracy_rate: number;
  }>;
}

export interface QuickStats {
  total_words: number;
  words_learned: number;
  total_study_time_minutes: number;
  recent_accuracy: number;
  streak_days: number;
} 