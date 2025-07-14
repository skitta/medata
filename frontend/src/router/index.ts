import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '@/views/LoginView.vue'),
  },
  {
    path: '/home',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ '@/views/HomeView.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import(/* webpackChunkName: "dashboard" */ '@/views/home/DashboardView.vue'),
      },
      {
        path: 'add',
        name: 'add',
        component: () => import(/* webpackChunkName: "add" */ '@/views/home/AddView.vue'),
        children: [
          {
            path: 'patient',
            name: 'add-patient',
            component: () => import(/* webpackChunkName: "add-patient" */ '@/views/home/add/AddPatientView.vue'),
            meta: { colSpan: 12 }
          },
          {
            path: 'tests',
            name: 'add-tests',
            component: () => import(/* webpackChunkName: "add-tests" */ '@/views/home/add/AddTestsView.vue'),
            meta: { colSpan: 16 }
          },
        ],
      },
      {
        path: 'manager',
        name: 'manager',
        component: () => import(/* webpackChunkName: "manager" */ '@/views/home/ManagerView.vue'),
      }
    ]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.isAuthenticated

  if (to.name !== 'login' && !isLoggedIn) {
    // 如果用户未登录且访问的不是登录页，则重定向到登录页
    next({ name: 'login' })
  } else if (to.name === 'login' && isLoggedIn) {
    // 如果用户已登录且访问的是登录页，则重定向到主页
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
