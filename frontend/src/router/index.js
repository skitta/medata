import { createRouter, createWebHashHistory } from 'vue-router'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
  },
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
        children: [
          {
            path: 'patient',
            name: 'add-patient',
            component: () => import('../views/home/add/AddPatientView.vue'),
            meta: { colSpan: 12 }
          },
          {
            path: 'tests',
            name: 'add-tests',
            component: () => import('../views/home/add/AddTestsView.vue'),
            meta: { colSpan: 16 }
          },
        ],
      },
      {
        path: 'manager',
        name: 'manager',
        component: () => import('../views/home/ManagerView.vue'),
      }
    ]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'login' && store.getters.getToken === null) { next({ name: 'login' }) }
  else { next() }
})

export default router
