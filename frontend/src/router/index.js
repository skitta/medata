import { createRouter, createWebHashHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import store from '@/store'

const routes = [
  {
    path: '/user',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
      }
    ]
  },
  {
    path: '/',
    name: 'login',
    component: LoginView,
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'login' && !store.getters.getToken) next({ name: 'login' })
  else next()
})

export default router
