export interface Word {
  id: number;
  jamaican_patois: string;
  english: string;
  parts?: {
    type: string;
    usage: string;
  };
  correct_count: number;
  wrong_count: number;
}

export interface PaginatedWords {
  words: Word[];
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
} 