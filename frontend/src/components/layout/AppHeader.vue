<template>
  <header class="app-header bg-white text-rem-primary shadow-sm border-b border-gray-200 w-full">
    <div class="w-full px-8">
      <div class="flex justify-between items-center py-4">

        <div class="flex items-center space-x-4">
          <div class="w-10 h-10 bg-rem-primary rounded-lg flex items-center justify-center">
            <span class="font-bold text-white text-sm">rem</span>
          </div>

          <div class="flex flex-col">
            <h1 class="text-lg font-bold tracking-tight">rem | F I N T E C H</h1>
            <p class="text-rem-secondary text-xs tracking-widest">T O O L S</p>
          </div>
        </div>

      

        <nav class="flex items-center space-x-4">
     
          <BaseButton   @click="logout"  variant="secondary">Cerrar Sesion</BaseButton>
        </nav>

      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import BaseButton from '../../components/ui/BaseButton.vue';
const router = useRouter();
const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};
</script>
