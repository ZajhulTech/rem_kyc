<template>
  <div class="flex justify-between items-start">
    <span class="text-sm font-medium text-gray-600">{{ label }}</span>
    <span v-if="$slots.default" class="text-sm text-gray-900 text-right flex-1 ml-4">
      <slot></slot>
    </span>
    <span v-else class="text-sm text-gray-900 text-right flex-1 ml-4">{{ value || 'No especificado' }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value?: string
}>();
</script>