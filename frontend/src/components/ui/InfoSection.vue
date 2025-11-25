<template>
  <div class="info-section">
    <h4 class="text-md font-semibold text-gray-900 mb-3">{{ title }}</h4>
    <div class="space-y-3">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
}>();
</script>