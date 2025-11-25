<template>
  <footer class="app-footer bg-white text-rem-primary border-t border-gray-200 w-full">
    <div class="w-full px-8 py-6">
      <div class="flex flex-col lg:flex-row justify-between items-center space-y-4 lg:space-y-0">

        <div class="text-center lg:text-left">
          <p class="font-bold text-sm">rem | FINTECH TOOLS</p>
         
        </div>

        <div class="text-center lg:text-right">
          <p class="text-rem-secondary text-xs">
            © {{ currentYear }} rem | FINTECH TOOLS. Todos los derechos reservados.
          </p>
        </div>

      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue';
const currentYear = computed(() => new Date().getFullYear());

</script>


