import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '@/views/DashboardView.vue';
import RegisterForm from "@/views/RegisterForm.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'principal', component: DashboardView },
    { path: '/dashboard', name: 'dashboard', component: DashboardView },
    { path: '/registro', name: 'register', component: RegisterForm },
    { path: '/verification/:id', name: 'VerificationDetail', component: () => import('@/views/VerificationDetailView.vue'),  props: true },
    { path: "/verification/:id/status", name: "changeVerificationStatus", component: () => import('@/views/ChangeVerificationStatus.vue'),  props: true }
   ]
});

export default router;
