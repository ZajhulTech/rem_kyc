<template>
  <MainLayout>
    <div class="w-full bg-white min-h-screen">
      <div class="flex w-full">
        <div class="flex-1 p-8">
          <div class="max-w-3xl mx-auto">

            <!-- Header -->
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-rem-primary">Cambiar Estatus</h2>

              <BaseButton 
                variant="secondary" 
                @click="$router.push(`/dashboard`)"
                class="flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Volver
              </BaseButton>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="text-center py-8">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rem-primary mx-auto"></div>
              <p class="mt-4 text-gray-600">Cargando información...</p>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {{ error }}
            </div>

            <!-- Detalle + Form -->
            <div v-else class="bg-white rounded-lg shadow-sm border border-gray-200">

              <!-- Header con Info -->
              <div class="border-b border-gray-200 px-6 py-4">
                <div class="flex justify-between items-center">
                  <h3 class="text-lg font-semibold text-gray-900">
                    {{ verification.full_name }}
                  </h3>
                  <StatusBadge :status="verification.status" :risk-level="verification.risk_level" />
                </div>
                <p class="text-gray-600 mt-1">{{ verification.email }}</p>
              </div>

              <!-- Formulario para cambiar estado -->
              <div class="p-6 space-y-6">

                <div>
                  <label class="block mb-2 text-sm font-medium text-gray-700">
                    Nuevo estatus
                  </label>

                  <select
                    v-model="selectedStatus"
                    class="w-full border border-gray-300 rounded-lg px-4 py-2 text-gray-700 focus:ring-rem-primary focus:border-rem-primary"
                  >
                    <option value="" disabled>Seleccione un estatus</option>
                    <option v-for="status in statuses" :key="status.code" :value="status.code">
                      {{ status.description }}
                    </option>
                  </select>
                </div>

                <div class="flex justify-end">
                  <BaseButton
                    variant="blueHover"
                    :disabled="updating"
                    @click="updateStatus"
                    class="flex items-center gap-2"
                  >
                    <svg v-if="updating" class="animate-spin w-4 h-4" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10"
                        stroke-width="4" />
                      <path class="opacity-75" stroke-width="4"
                        d="M4 12a8 8 0 018-8v8z" />
                    </svg>
                    Actualizar Estatus
                  </BaseButton>
                </div>

                <!-- Mensaje de éxito -->
                <p v-if="successMessage" class="text-green-600 font-medium">
                  {{ successMessage }}
                </p>

                <p v-if="formError" class="text-red-600 text-sm mt-1">
                  {{ formError }}
                </p>

              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import MainLayout from "@/components/layout/MainLayout.vue";
import BaseButton from "@/components/ui/BaseButton.vue";
import StatusBadge from "@/components/ui/StatusBadge.vue";

import { getVerificationById, updateVerificationStatus } from "@/services/verificationService";
import { getStatusVerification } from "@/services/catalogService";
import type { VerificationDetailResponseDTO, VerificationStatusResponseDTO } from "@/services/types";

const route = useRoute();
const verificationId = route.params.id as string;

const verification = ref<VerificationDetailResponseDTO | null>(null);
const statuses = ref<VerificationStatusResponseDTO[]>([]);
const selectedStatus = ref("");

const loading = ref(true);
const updating = ref(false);
const error = ref("");
const successMessage = ref("");

const formError = ref("");

onMounted(async () => {
  try {
    loading.value = true;

    const detailResponse = await getVerificationById(verificationId);
    if (detailResponse.success) {
      verification.value = detailResponse.data;
    }

    const statusResponse = await getStatusVerification();
    statuses.value = statusResponse;

  } catch (err: any) {
    error.value = "No se pudo cargar la información.";
  } finally {
    loading.value = false;
  }
});

async function updateStatus() {

  formError.value = "";

  if (!selectedStatus.value) {
     formError.value = "Debes seleccionar un nuevo estado antes de continuar.";
     return;
  }

  if (selectedStatus.value === verification.value?.status) {
    formError.value = "Debes seleccionar un estado diferente al actual.";
    return;
}

  try {
    updating.value = true;
    successMessage.value = "";

    const payload = {
      verification_id: verificationId,
      status_code: selectedStatus.value
    };

    const response = await updateVerificationStatus(payload);

    if (response.success) {
      successMessage.value = "Estatus actualizado correctamente";

      // Actualiza el badge en pantalla
      verification.value!.status = selectedStatus.value;
    }

  } catch (err: any) {
    error.value = err.response?.data?.message || "Error al actualizar.";
  } finally {
    updating.value = false;
  }
}
</script>
