export interface StudySession {
  id: number;
  activity_name: string;
  group_name: string;
  start_time: string;
  end_time: string | null;
  review_items_count: number;
}

export interface PaginatedSessions {
  study_sessions: StudySession[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
} 