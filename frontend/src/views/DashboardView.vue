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
                v-model="name"
              />
              <BaseButton variant="secondary" @click="getVerificationfromServ">Actualizar</BaseButton>
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
              @row:edit="(row) => console.log('Editar fila de:', row)"
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

  const items = ref([]);
  const totalPages = ref(0);
  const page = ref(1);
  const pageSize = ref(10);

  async function loadDataTable(p: number = 1) {
    try {
      const response = await getVerifications(p, pageSize.value);
      items.value = response.items.map(item => ({
        id: item.id,
        name: item.full_name,
        email: item.email,
        country: item.country,
        status: item.status === "approved" ? "✅ Aprobado"
              : item.status === "pending" ? "⚠️ Pendiente"
              : "❌ Rechazado",
        createdAt: formatDate(item.created_at)
      }));
      totalPages.value = response.total_pages;
      page.value = response.page;

      console.log("Pagina:",page.value);
      console.log("Totales:",totalPages.value);
      console.log("Data Item:", items.value);

    } catch (error) {
      console.error("Error al cargar verificaciones:", error);
    }
  }  

  onMounted(() => loadDataTable(page.value));

</script>
