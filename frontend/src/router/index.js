import { createRouter, createWebHashHistory } from 'vue-router'
import store from '@/store'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../views/home/DashboardView.vue'),
      },
      {
        path: 'add',
        name: 'add',
        component: () => import('../views/home/AddView.vue'),
      },
      {
        path: 'manager',
        name: 'manager',
        component: () => import('../views/home/ManagerView.vue'),
      }
    ]
  },
  {
    path: '/',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
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
