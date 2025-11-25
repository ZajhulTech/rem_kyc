#D:\Lab\Onboarding_KYC\frontend\src\views\RegisterForm.vue
<template>
    <MainLayout>
    <div class="w-full bg-white min-h-screen">
        <div class="flex w-full">
        <!-- Contenido -->
        <div class="flex-1 p-8">
            <h2 class="text-2xl font-bold text-rem-primary mb-4">Solicitud de Verificación</h2>
        
            <form 
                @submit.prevent="handleSubmit"
                class="space-y-6 bg-white p-8 rounded-xl  max-w-xl mx-auto mb-8"
            >
                <!-- FULL NAME -->
                <BaseInput
                label="Nombre completo"
                placeholder="Ej. Juan Pérez"
                v-model="form.full_name"
                :error="errors.full_name"
                />

                <!-- EMAIL -->
                <BaseInput
                label="Correo electrónico"
                type="email"
                placeholder="usuario@correo.com"
                v-model="form.email"
                :error="errors.email"
                />

                <!-- PHONE -->
                <BaseInput
                label="Teléfono"
                placeholder="Ej. 5512345678"
                v-model="form.phone"
                :error="errors.phone"
                />

                <!-- COUNTRY -->
                <div>
                    <label class="block mb-1 text-sm font-medium text-rem-primary">
                        País
                    </label>
                    <select
                        v-model="form.country_code"
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white
                            focus:ring-2 focus:ring-rem-primary focus:border-rem-primary"
                    >
                        <option value="" disabled>Selecciona un país</option>
                        <option v-for="c in countries" :key="c.id" :value="c.code">
                        {{ c.name }}
                        </option>
                    </select>
                    <p v-if="errors.country_code" class="text-rem-accent text-xs mt-1 text-red-800">
                        {{ errors.country_code }}
                    </p>
                </div>

                <!-- DOCUMENT TYPE -->
                <div>
                    <label class="block mb-1 text-sm font-medium text-rem-primary">
                        Tipo de documento
                    </label>
                    <select
                        v-model="form.document_type_code"
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 bg-white
                            focus:ring-2 focus:ring-rem-primary focus:border-rem-primary"
                    >
                        <option value="" disabled>Selecciona un documento</option>
                        <option v-for="t in docTypes" :key="t.id" :value="t.code">
                        {{ t.description }}
                        </option>
                    </select>
                    <p v-if="errors.document_type_code" class="text-rem-accent text-xs mt-1 text-red-800">
                        {{ errors.document_type_code }}
                    </p>
                </div>

                <!-- DOCUMENT NUMBER -->
                <BaseInput
                label="Número de documento"
                placeholder="Ej. 123456789"
                v-model="form.document_number"
                :error="errors.document_number"
                />

                <!-- DOCUMENT IMAGE -->
                <div>
                <label class="block mb-1 text-sm font-medium text-rem-primary">
                    Foto del documento
                </label>
                <input 
                    type="file"
                    accept="image/*"
                    @change="(e) => handleImageUpload(e, 'document_image')"
                    class="block w-full text-sm"
                    :disabled="isSubmitting"
                />
                <p v-if="errors.document_image" class="text-rem-accent text-xs mt-1">
                    {{ errors.document_image }}
                </p>

                <img 
                    v-if="preview.document_image"
                    :src="preview.document_image"
                    class="mt-2 w-32 h-32 object-cover rounded-lg shadow"
                />
                </div>

                <!-- SELFIE IMAGE -->
                <div>
                <label class="block mb-1 text-sm font-medium text-rem-primary">
                    Selfie
                </label>
                <input 
                    type="file"
                    accept="image/*"
                    @change="(e) => handleImageUpload(e, 'selfie_image')"
                    class="block w-full text-sm"
                    :disabled="isSubmitting"
                />
                <p v-if="errors.selfie_image" class="text-rem-accent text-xs mt-1">
                    {{ errors.selfie_image }}
                </p>

                <img 
                    v-if="preview.selfie_image"
                    :src="preview.selfie_image"
                    class="mt-2 w-32 h-32 object-cover rounded-lg shadow"
                />
                </div>

                <!-- SUBMIT BUTTON -->
                <BaseButton
                    class="w-full"
                    variant="blueHover"
                    type="submit"
                    :disabled="isSubmitting"
                >
                    <span v-if="isSubmitting">Enviando...</span>
                    <span v-else>Registrar Solicitud</span>
                </BaseButton>
            </form>

            <!-- Alertas -->
            
            <div v-if="errorMessage" class="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                {{ errorMessage }}
            </div>

            
            <div v-if="successMessage" class="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
                {{ successMessage }}
            </div>
            
        </div>
        </div>
    </div>
    </MainLayout>
</template>

<script setup lang="ts">
    import { reactive, ref, onMounted } from "vue";
    import BaseInput from "@/components/ui/BaseInput.vue";
    import BaseButton from '@/components/ui/BaseButton.vue';
    import MainLayout from '@/components/layout/MainLayout.vue';
    import { getCountries, getDocumentTypes } from "@/services/catalogService";
    import { createVerification } from "@/services/verificationService";
    import type { VerificationRequestDTO } from "@/services/types";

    // Datos del formulario
    const form = reactive({
        full_name: "",
        email: "",
        phone: "",
        country_code: "",
        document_type_code: "",
        document_number: "",
        document_image: null as File | null,
        selfie_image: null as File | null
    });

    // Vistas previas de imágenes
    const preview = reactive({
        document_image: null as string | null,
        selfie_image: null as string | null
    });

    const countries = ref([]);
    const docTypes = ref([]);
    
    // Estados
    const errors = reactive<any>({});
    const isSubmitting = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");

    // Cargar catálogos
    async function loadCountries() {
        try {
            const response = await getCountries();
            countries.value = response.map((c: any) => ({
                id: c.id,
                code: c.code,
                name: c.name
            }));
        } catch (error) {
            console.error("Error al cargar países", error);
            errorMessage.value = "Error al cargar la lista de países";
        }
    }

    async function loadDocumentTypes() {
        try {
            const response = await getDocumentTypes();
            docTypes.value = response.map((t: any) => ({
                id: t.id,
                code: t.code,
                description: t.description
            }));
        } catch (error) {
            console.error("Error al cargar tipos de documento", error);
            errorMessage.value = "Error al cargar los tipos de documento";
        }
    }

    onMounted(() => {
        loadCountries();
        loadDocumentTypes();
    });

    // Validación
    function validate() {
        // Limpiar errores anteriores
        Object.keys(errors).forEach(key => delete errors[key]);
        
        errors.full_name = form.full_name ? "" : "El nombre es obligatorio.";
        errors.email = /\S+@\S+\.\S+/.test(form.email) ? "" : "Correo inválido.";
        errors.phone = form.phone.length >= 8 ? "" : "Teléfono inválido.";
        errors.country_code = form.country_code ? "" : "Selecciona un país.";
        errors.document_type_code = form.document_type_code ? "" : "Selecciona un documento.";
        errors.document_number = form.document_number ? "" : "Campo obligatorio.";
        errors.document_image = form.document_image ? "" : "La foto del documento es obligatoria.";
        errors.selfie_image = form.selfie_image ? "" : "La selfie es obligatoria.";

        return Object.values(errors).every((e) => e === "");
    }

    // Manejo de imágenes
    function handleImageUpload(event: any, key: 'document_image' | 'selfie_image') {
        const file = event.target.files[0];
        if (!file) return;

        // Validar tipo de archivo
        if (!file.type.startsWith('image/')) {
            errors[key] = "Por favor selecciona un archivo de imagen válido.";
            return;
        }

        // Validar tamaño (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            errors[key] = "La imagen no debe superar los 5MB.";
            return;
        }

        form[key] = file;
        preview[key] = URL.createObjectURL(file);
        errors[key] = ""; // Limpiar error si había uno
    }

    // Función para subir imagen y obtener URL
    async function uploadImage(file: File): Promise<string> {
        // TODO: Implementar la subida real a tu servicio de almacenamiento
        // Por ahora simulamos una URL temporal
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(`https://storage.kyc.com/temp/${file.name}-${Date.now()}`);
            }, 500);
        });
    }

    // Submit
    async function handleSubmit() {
        // Limpiar mensajes anteriores
        successMessage.value = "";
        errorMessage.value = "";

        if (!validate()) {
            errorMessage.value = "Por favor corrige los errores del formulario.";
            return;
        }

        isSubmitting.value = true;

        try {
            // Subir imágenes y obtener URLs
            const [documentUrl, selfieUrl] = await Promise.all([
                uploadImage(form.document_image!),
                uploadImage(form.selfie_image!)
            ]);

            // Preparar payload para la API
            const payload: VerificationRequestDTO = {
                full_name: form.full_name,
                email: form.email,
                phone: form.phone,
                country_code: form.country_code,
                document_type_code: form.document_type_code,
                document_number: form.document_number,
                document_image_url: documentUrl,
                selfie_image_url: selfieUrl
            };

            // Enviar a la API
            const response = await createVerification(payload);
            
            successMessage.value = response.message || "Solicitud enviada con éxito.";
            
            // Resetear formulario
            resetForm();
            
        } catch (error: any) {
            console.error("Error al enviar solicitud:", error);
            errorMessage.value = error.response?.data?.message || "Error al enviar la solicitud. Por favor intenta nuevamente.";
        } finally {
            isSubmitting.value = false;
        }
    }

    // Resetear formulario
    function resetForm() {
        form.full_name = "";
        form.email = "";
        form.phone = "";
        form.country_code = "";
        form.document_type_code = "";
        form.document_number = "";
        form.document_image = null;
        form.selfie_image = null;
        
        preview.document_image = null;
        preview.selfie_image = null;
        
        // Limpiar errores
        Object.keys(errors).forEach(key => delete errors[key]);
    }
</script>