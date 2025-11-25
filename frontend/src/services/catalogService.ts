// src/services/catalogService.ts
import api from "./api";
import type { ApiResponse, CountryResponseDTO, DocumentTypeResponseDTO  } from "./types";


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