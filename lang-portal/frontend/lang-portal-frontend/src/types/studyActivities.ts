export interface StudyActivity {
  id: number;
  name: string;
  study_session_id: number | null;
  group_id: number;
  created_at: string;
  group_name: string;
  review_items_count: number;
}

export interface StudyActivityCreate {
  name: string;
  group_id: number;
} 