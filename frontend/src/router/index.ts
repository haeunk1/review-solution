import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/',
      component: DashboardLayout,
      children: [
        { path: '', name: 'index', component: () => import('@/views/IndexView.vue') },
        { path: 'reviews', name: 'reviews', component: () => import('@/views/ReviewsView.vue') },
        { path: 'alerts', name: 'alerts', component: () => import('@/views/AlertsView.vue') },
        { path: 'statistics', name: 'statistics', component: () => import('@/views/StatisticsView.vue') },
        { path: 'competitors', name: 'competitors', component: () => import('@/views/CompetitorsView.vue') },
        { path: 'reports', name: 'reports', component: () => import('@/views/ReportsView.vue') },
        { path: 'requests', name: 'requests', component: () => import('@/views/ReviewRequestView.vue') },
        { path: 'settings', name: 'settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const hospitalId = localStorage.getItem('hospital_id')
  if (to.name !== 'login' && !hospitalId) {
    return { name: 'login' }
  }
  if (to.name === 'login' && hospitalId) {
    return { name: 'index' }
  }
})

export default router
