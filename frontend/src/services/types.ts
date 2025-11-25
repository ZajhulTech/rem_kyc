
export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string | null;
  data: T;
}


export interface VerificationResponseDTO {
  id: string;
  full_name: string;
  email: string;
  country: string;
  status: string;
  created_at: string;

}

export interface VerificationDetailResponseDTO {
  id: string;
  full_name: string;
  email: string;
  phone: string;
  country: string;
  document_type: string;
  document_number: string;
  document_image_url?: string;
  selfie_image_url?: string;
  status: string;
  risk_score?: number;
  risk_level: string;
  created_at: string;
  updated_at: string; 
}

export interface VerificationRequestDTO {

  full_name: string;
  email: string;
  phone: string;
  country_code: string;
  document_type_code: string;
  document_number: string;
  document_image_url?: string;
  selfie_image_url?: string;
}

export interface CountryResponseDTO {
  id: string;
  code: string;
  name: string;
  calling_code: string;
  created_at: string;
  updated_at: string;
}

export interface DocumentTypeResponseDTO {
  id: string;
  code: string;
  description: string;
}