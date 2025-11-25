
<template>
  <div class="w-full">
    <label v-if="label" class="block mb-1 text-sm font-medium text-rem-primary">
      {{ label }}
    </label>

    <input
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full px-4 py-2 rounded-lg border 
             border-gray-300 focus:outline-none focus:ring-2 
             focus:ring-rem-primary focus:border-rem-primary 
             transition-all bg-white text-rem-text"
    />

    <p v-if="error" class="text-rem-accent text-xs mt-1 text-red-800">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps({
  label: String,
  placeholder: String,
  type: { type: String, default: "text" },
  modelValue: String,
  error: String
});
defineEmits(["update:modelValue"]);
</script>
