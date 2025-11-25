<template>
  <div class="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">

    <!-- Loading Skeleton -->
    <div v-if="loading" class="p-4 space-y-3 animate-pulse">
      <div class="h-4 bg-gray-200 rounded w-1/3"></div>
      <div class="h-4 bg-gray-200 rounded w-full"></div>
      <div class="h-4 bg-gray-200 rounded w-4/5"></div>
      <div class="h-4 bg-gray-200 rounded w-2/3"></div>
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-left text-sm">

        <!-- HEADERS -->
        <thead class="bg-rem-primary text-black !text-black">
          <tr>
            <th
              v-for="header in headers"
              :key="header"
              class="px-4 py-3 font-semibold uppercase text-black !text-black tracking-wide text-xs"
            >
              {{ header }}
            </th>

            <!-- Actions column -->
            <th class="px-4 py-3 font-semibold uppercase tracking-wide text-xs text-black !text-black">
              Acciones
            </th>
          </tr>
        </thead>

        <!-- BODY -->
        <tbody>
          <tr
            v-for="row in paginatedRows"
            :key="row[idField]"
            class="border-b hover:bg-gray-50 transition"
          >
            <td v-for="field in fields" :key="field" class="px-4 py-3 text-rem-text">
              {{ row[field] }}
            </td>

            <!-- ACTION BUTTONS -->
            <td class="px-4 py-3 flex gap-2">

                <button
                @click="$emit('row:view', row)"
                class="px-3 py-1 rounded-lg bg-blue-400 text-white text-xs hover:bg-blue-700"
              >
                Detalle
              </button>
              
              <button
                @click="$emit('row:edit', row)"
                class="px-3 py-1 rounded-lg bg-green-400 text-white text-xs hover:bg-green-700"
              >
                Editar
              </button>

            </td>
          </tr>

          <!-- No data -->
          <tr v-if="items.length === 0">
            <td :colspan="fields.length + 1" class="text-center py-6 text-gray-500">
              No hay datos para mostrar
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- PAGINATION -->
    <div class="flex justify-between items-center p-4 bg-gray-50 border-t">
      
      <p class="text-xs text-gray-600">
        Página {{ currentPage }} de {{ totalPages }}
      </p>

      <div class="flex gap-2">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-3 py-1 text-xs rounded-lg border disabled:opacity-40"
        >
          Anterior
        </button>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 text-xs rounded-lg border disabled:opacity-40"
        >
          Siguiente
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref } from "vue";

  const props = defineProps({
    headers: Array,
    fields: Array,
    items: { type: Array, default: () => [] },
    idField: { type: String, default: "id" },
    pageSize: { type: Number, default: 5 },
    loading: { type: Boolean, default: false },
    totalPages:{ type: Number, default: 0 },
    page:{ type:Number, default: 0 },
  });

  const emit = defineEmits(["update:page"]);

  // Pagination
  const currentPage = computed(() => props.page);
/*
  const totalPages = computed(() =>
    Math.ceil(props.items.length / props.pageSize)
  );
*/

  const paginatedRows = computed(() => props.items);

  const nextPage = () => {
    if (props.page < props.totalPages) {
      emit("update:page", props.page + 1);
    }
  };

  const prevPage = () => {
    if (props.page > 1) {
      emit("update:page", props.page - 1);
    }
  };
  
</script>
