<template>
  <div class="main-layout h-screen flex flex-col bg-white">
    <!-- HEADER -->
    <AppHeader />

    <!-- BODY -->
    <div class="flex flex-1 overflow-hidden">

      <!-- SIDEBAR -->
      <aside class="w-64 bg-rem-primary text-white flex flex-col p-4 space-y-2">
      <h2 class="text-lg font-semibold mb-4">Menú</h2>

      <!-- Dashboard -->
      <router-link
        to="/dashboard"
        class="menu-item menu-item-inactive group"
        active-class="menu-item-active"
        
      >
        📊 Dashboard
      </router-link>

      <!-- Registro -->
      <router-link
        to="/registro"
        class="menu-item menu-item-inactive group"
        active-class="menu-item-active"
      >
        📝 Solicitud de verificación
      </router-link>

      </aside>

      <!-- MAIN CONTENT -->
      <main class="flex-1 p-6 overflow-y-auto bg-rem-light">
        <slot />
      </main>
    </div>

    <!-- FOOTER -->
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
  import AppHeader from './AppHeader.vue';
  import AppFooter from './AppFooter.vue';
</script>

<style scoped lang="postcss">

</style>
