<template>
  <div class="flex items-center gap-2">
    <span :class="statusClass" class="px-3 py-1 rounded-full text-xs font-medium">
      {{ statusText }}
    </span>
    <span :class="riskClass" class="px-3 py-1 rounded-full text-xs font-medium">
      {{ riskText }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  status: string
  riskLevel: string
}>();

const statusClass = computed(() => {
  const classes: Record<string, string> = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'approved': 'bg-green-100 text-green-800',
    'rejected': 'bg-red-100 text-red-800',
    'requires_information': 'bg-blue-100 text-blue-800'
  };
  return classes[props.status] || 'bg-gray-100 text-gray-800';
});

const statusText = computed(() => {
  const texts: Record<string, string> = {
    'pending': 'Pendiente',
    'approved': 'Aprobado',
    'rejected': 'Rechazado',
    'requires_information': 'Requiere Info'
  };
  return texts[props.status] || props.status;
});

const riskClass = computed(() => {
  const classes: Record<string, string> = {
    'low': 'bg-green-100 text-green-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'high': 'bg-red-100 text-red-800',
    'n/c': 'bg-gray-100 text-gray-800'
  };
  return classes[props.riskLevel] || 'bg-gray-100 text-gray-800';
});

const riskText = computed(() => {
  const texts: Record<string, string> = {
    'low': 'Bajo Riesgo',
    'medium': 'Riesgo Medio',
    'high': 'Alto Riesgo',
    'n/c': 'Por evaluar'
  };
  return texts[props.riskLevel] || props.riskLevel;
});
</script>