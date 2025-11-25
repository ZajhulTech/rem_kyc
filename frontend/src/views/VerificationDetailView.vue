<template>
  <MainLayout>
    <div class="w-full bg-white min-h-screen">
      <div class="flex w-full">
        <!-- Contenido -->
        <div class="flex-1 p-8">
          <div class="max-w-4xl mx-auto">
            <!-- Header -->
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-rem-primary">Detalle de Verificación</h2>
              <BaseButton 
                variant="secondary" 
                @click="$router.push(`/dashboard`)"

                class="flex items-center gap-2"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
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
              <p>{{ error }}</p>
            </div>

            <!-- Detalle de verificación -->
            <div v-else-if="verification" class="bg-white rounded-lg shadow-sm border border-gray-200">
              <!-- Header con estado -->
              <div class="border-b border-gray-200 px-6 py-4">
                <div class="flex justify-between items-center">
                  <h3 class="text-lg font-semibold text-gray-900">
                    {{ verification.full_name }}
                  </h3>
                  <StatusBadge :status="verification.status" :risk-level="verification.risk_level" />
                </div>
                <p class="text-gray-600 mt-1">{{ verification.email }}</p>
              </div>
             
              <!-- Información principal -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
                
                <!-- Columna izquierda -->
                <div class="space-y-6">
                   
                  <!-- Información personal -->
                  <InfoSection title="Información Personal">
                    <InfoField label="Nombre completo" :value="verification.full_name" />
                    <InfoField label="Email" :value="verification.email" />
                    <InfoField label="Teléfono" :value="verification.phone" />
                    <InfoField label="País" :value="verification.country" />
                  </InfoSection>

                  <!-- Información del documento -->
                  <InfoSection title="Documento de Identificación">
                    <InfoField label="Tipo de documento" :value="verification.document_type" />
                    <InfoField label="Número de documento" :value="verification.document_number" />
                  </InfoSection>
                </div>

                <!-- Columna derecha -->
                <div class="space-y-6">
                  <!-- Estado y riesgo -->
                  <InfoSection title="Estado y Análisis">
                    <InfoField label="Estado">
                      <span :class="statusClass(verification.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                        {{ statusText(verification.status) }}
                      </span>
                    </InfoField>
                    <InfoField label="Nivel de riesgo">
                      <span :class="riskLevelClass(verification.risk_level)" class="px-2 py-1 rounded-full text-xs font-medium">
                        {{ riskLevelText(verification.risk_level) }}
                      </span>
                    </InfoField>
                    <InfoField 
                      label="Puntaje de riesgo" 
                      :value="verification.risk_score !== null ? verification.risk_score.toString() : 'No evaluado'" 
                    />
                  </InfoSection>

                  <!-- Fechas -->
                  <InfoSection title="Fechas">
                    <InfoField label="Fecha de creación" :value="formatDate(verification.created_at)" />
                    <InfoField label="Última actualización" :value="formatDate(verification.updated_at)" />
                  </InfoSection>
                </div>
              </div>

              <!-- Imágenes -->
              <div class="border-t border-gray-200 px-6 py-6">
                <h4 class="text-lg font-semibold text-gray-900 mb-4">Documentación</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- Documento -->
                  <div>
                    <h5 class="font-medium text-gray-700 mb-3">Documento de identificación</h5>
                    <div class="border border-gray-300 rounded-lg p-4">
                      <img 
                        v-if="verification.document_image_url"
                        :src="verification.document_image_url" 
                        alt="Documento de identificación"
                        class="w-full h-64 object-contain rounded"
                        @error="handleImageError"
                      />
                      <div v-else class="text-center py-8 text-gray-500">
                        <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Imagen no disponible
                      </div>
                    </div>
                  </div>

                  <!-- Selfie -->
                  <div>
                    <h5 class="font-medium text-gray-700 mb-3">Selfie</h5>
                    <div class="border border-gray-300 rounded-lg p-4">
                      <img 
                        v-if="verification.selfie_image_url"
                        :src="verification.selfie_image_url" 
                        alt="Selfie"
                        class="w-full h-64 object-contain rounded"
                        @error="handleImageError"
                      />
                      <div v-else class="text-center py-8 text-gray-500">
                        <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        Imagen no disponible
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import MainLayout from '@/components/layout/MainLayout.vue';
import BaseButton from '@/components/ui/BaseButton.vue';
import InfoSection from '@/components/ui/InfoSection.vue';
import InfoField from '@/components/ui/InfoField.vue';
import StatusBadge from '@/components/ui/StatusBadge.vue';
import { getVerificationById } from '@/services/verificationService';
import type { VerificationDetailResponseDTO } from '@/services/types';



// Lógica del componente
const route = useRoute();
const verification = ref<VerificationDetailResponseDTO | null>(null);
const loading = ref(true);
const error = ref('');

// Obtener ID de la URL
const verificationId = route.params.id as string;

// Funciones de utilidad
function statusClass(status: string) {
  const classes = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'approved': 'bg-green-100 text-green-800',
    'rejected': 'bg-red-100 text-red-800',
    'requires_information': 'bg-blue-100 text-blue-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
}

function statusText(status: string) {
  const texts = {
    'pending': 'Pendiente',
    'approved': 'Aprobado',
    'rejected': 'Rechazado',
    'requires_information': 'Requiere Información'
  };
  return texts[status] || status;
}

function riskLevelClass(riskLevel: string) {
  const classes = {
    'low': 'bg-green-100 text-green-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'high': 'bg-red-100 text-red-800',
    'n/c': 'bg-gray-100 text-gray-800'
  };
  return classes[riskLevel] || 'bg-gray-100 text-gray-800';
}

function riskLevelText(riskLevel: string) {
  const texts = {
    'low': 'Bajo',
    'medium': 'Medio',
    'high': 'Alto',
    'n/c': 'No evaluado'
  };
  return texts[riskLevel] || riskLevel;
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function handleImageError(event: Event) {
  const target = event.target as HTMLImageElement;
  target.style.display = 'none';
  // Podrías mostrar un placeholder aquí
}

// Cargar datos
onMounted(async () => {
  try {
    loading.value = true;
    const response = await getVerificationById(verificationId);
    
    console.log('Respuesta de la verificación:', response);

    if (response.success && response.data) {
      verification.value = response.data;
    } else {
      error.value = response.message || 'No se pudo cargar la verificación';
    }
  } catch (err: any) {
    console.error('Error al cargar verificación:', err);
    error.value = err.response?.data?.message || 'Error al cargar los datos de la verificación';
  } finally {
    loading.value = false;
  }
});
</script>