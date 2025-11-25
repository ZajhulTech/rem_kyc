<template>
  <button
    :type="type"
    :class="[
      'px-4 py-2 rounded-lg font-medium text-sm transition-colors duration-200 shadow-sm',
      variantClasses
    ]"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps({
  type: { type: String, default: "button" },
  variant: {
    type: String,
    default: "primary", // primary, secondary, danger
  },
});

const variantClasses = {
  primary: "bg-rem-primary text-white hover:bg-opacity-90",
  secondary: "bg-gray-100 text-rem-primary hover:bg-gray-200 border border-gray-300",
  danger: "bg-rem-accent text-white hover:bg-red-600",
  blueHover: "bg-gray-100 text-rem-primary hover:bg-blue-900 hover:text-white border border-gray-300"
}[props.variant];
</script>
