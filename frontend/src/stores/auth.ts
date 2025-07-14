import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { TokenStorage } from '@/utils/tokenStorage'
import { getToken } from '@/api/login'
import type { LoginRequest } from '@/types/api'
import { useMainStore } from '@/stores'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(TokenStorage.isTokenValid())
  const router = useRouter()

  async function login(credentials: LoginRequest) {
    try {
      const token = await getToken(credentials.username, credentials.password)
      TokenStorage.setToken(token)
      isAuthenticated.value = true
      await router.push({ name: 'home' })
    } catch (error) {
      isAuthenticated.value = false
      throw error
    }
  }

  async function logout() {
    const mainStore = useMainStore()
    mainStore.clearState()
    TokenStorage.clearToken()
    isAuthenticated.value = false
    await router.push({ name: 'login' })
  }

  return {
    isAuthenticated,
    login,
    logout,
  }
})
