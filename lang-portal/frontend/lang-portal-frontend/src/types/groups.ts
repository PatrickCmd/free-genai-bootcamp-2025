export interface Group {
  id: number;
  name: string;
  word_count: number;
  description: string | null;
}

export interface PaginatedGroups {
  groups: Group[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
} 