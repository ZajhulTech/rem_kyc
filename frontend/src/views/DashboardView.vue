<template>
  <MainLayout>
    <div class="w-full bg-white min-h-screen">
      <div class="flex w-full">
        
        <!-- Contenido -->
        <div class="flex-1 p-8">
          <h2 class="text-2xl font-bold text-rem-primary mb-4">Dashboard Principal</h2>
           
          <div class="mb-8">
        
             <nav class="flex items-center space-x-4">
              <BaseInput
                label=""
                placeholder="Busqueda por Nombre o Estatus"
                v-model="searchText"
              />
               <BaseButton variant="secondary" @click="handleSearch">
                {{ loading ? 'Buscando...' : 'Buscar' }}
              </BaseButton>
            </nav>

          </div>

          <div class="mb-8">
            <BaseTable 
              :headers="headers"
              :fields="fields"
              :items="items"
              :page="page"
              :pageSize="pageSize"
              :totalPages="totalPages"
              @update:page="loadDataTable"
              @row:view="(row) => router.push(`/verification/${row.id}`)"
              @row:edit="(row) => $router.push(`/verification/${row.id}/status`)"
            />
          </div>
        </div>

      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
  import MainLayout from '@/components/layout/MainLayout.vue';
  import BaseButton from '@/components/ui/BaseButton.vue';
  import BaseInput from '@/components/ui/BaseInput.vue';
  import BaseTable from '@/components/ui/BaseTable.vue';
  import { ref, onMounted } from "vue";
  import { getVerifications } from "@/services/verificationService";

  import { formatDate } from '@/infra/utils';

  import { useRouter } from 'vue-router';

  const router = useRouter();

  const headers = [
      "Nombre",
      "Email",
      "País",
      "Estado",
      "Fecha de creación"
  ];
  const fields = [
    "name",
    "email",
    "country",
    "status",
    "createdAt"
  ];

  const loading = ref(false);
  const searchText = ref('');

  const items = ref([]);
  const totalPages = ref(0);
  const page = ref(1);
  const pageSize = ref(10);

  async function loadDataTable(p: number = 1) {
    try {
      loading.value = true;
      const response = await getVerifications(p, pageSize.value, searchText.value);
      items.value = response.items.map(item => ({
        id: item.id,
        name: item.full_name,
        email: item.email,
        country: item.country,
        status: item.status === "approved" ? "✅ Aprobado"
              : item.status === "pending" ? "⚠️ Pendiente"
              : item.status === "requires_information" ? "ℹ️ Requiere Información"
              : "❌ Rechazado",
        createdAt: formatDate(item.created_at)
      }));
      totalPages.value = response.total_pages;
      page.value = response.page;

    } catch (error) {
      console.error("Error al cargar verificaciones:", error);
    }
    finally {
      loading.value = false;
    }
  }  

  const handleSearch = () => {
    page.value = 1; 
    loadDataTable();
  };

  const clearSearch = () => {
    searchText.value = '';
    page.value = 1;
    loadDataTable();
  } ;

  onMounted(() => loadDataTable(page.value));

</script>
