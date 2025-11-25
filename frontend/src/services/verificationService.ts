import api from "./api";
import type { ApiResponse, PaginatedResult, VerificationResponseDTO, VerificationDetailResponseDTO, VerificationRequestDTO, UpdateVerificationStatusDTO } from "./types";


export async function getVerifications(page = 1, pageSize = 10, filter = "") {
  
   const baseURL = `/verification?page=${page}&page_size=${pageSize}` + (filter != "" ? `&filter=${filter}` : "");
  
   const response = await api.get<ApiResponse<PaginatedResult<VerificationResponseDTO>>>( baseURL);

   return {
    items: response.data.data.items,
    total: response.data.data.total,
    page: response.data.data.page,
    page_size: response.data.data.page_size,
    total_pages: response.data.data.total_pages
    };
  
}

export async function getVerificationById(id: string) {
  const response = await api.get<ApiResponse<VerificationDetailResponseDTO>>(`/verification/detail?id=${id}`);
  return response.data;
}

export async function createVerification(payload: VerificationRequestDTO) {
  const response = await api.post<ApiResponse<VerificationResponseDTO>>(
    "/verification",
    payload
  );

  return response.data;
}

export async function updateVerificationStatus(payload: UpdateVerificationStatusDTO) {
  const response = await api.put("/verification/status", payload);
  return response.data;
}


