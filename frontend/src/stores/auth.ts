import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { TokenStorage } from '@/utils/tokenStorage'
import { getToken } from '@/api/login'
import type { LoginRequest } from '@/types/api'
import { useMainStore } from '@/stores'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(TokenStorage.isTokenValid())
  const fullName = ref(TokenStorage.getUsername() || '') // Now stores full name
  const router = useRouter()

  async function login(credentials: LoginRequest) {
    try {
      const response = await getToken(credentials.username, credentials.password)
      TokenStorage.setToken(response.token)
      TokenStorage.setUsername(response.full_name) // Store full name from API response
      isAuthenticated.value = true
      fullName.value = response.full_name
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
    TokenStorage.clearUsername()
    isAuthenticated.value = false
    fullName.value = ''
    await router.push({ name: 'login' })
  }

  return {
    isAuthenticated,
    fullName,
    login,
    logout,
  }
})
