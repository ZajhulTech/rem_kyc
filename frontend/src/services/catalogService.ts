// src/services/catalogService.ts
import api from "./api";
import type { ApiResponse, CountryResponseDTO, DocumentTypeResponseDTO, VerificationStatusResponseDTO  } from "./types";


export async function getCountries() {
  const response = await api.get<ApiResponse<CountryResponseDTO[]>>(
    "/catalogs/countries"
  );

  return response.data.data;
};

export async function getDocumentTypes() {
  const response = await api.get<ApiResponse<DocumentTypeResponseDTO[]>>(
    "/catalogs/document-types"
  );

  return response.data.data;
};

export async function getStatusVerification() {
  const response = await api.get<ApiResponse<VerificationStatusResponseDTO[]>>(
    "/catalogs/verification-statuses"
  );

  return response.data.data;
};