import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { TokenStorage } from '@/utils/tokenStorage'
import { UserStorage } from '@/utils/userStorage'
import { getToken } from '@/api/login'
import type { LoginRequest } from '@/types/api'
import { useMainStore } from '@/stores'

export const useAuthStore = defineStore('auth', () => {
  const userInfo = ref(UserStorage.getUserInfo())
  const isAuthenticated = ref(TokenStorage.isTokenValid() && userInfo.value !== null)
  const fullName = ref(userInfo.value?.fullName || '')
  const userId = ref(userInfo.value?.id || null)
  const router = useRouter()

  async function login(credentials: LoginRequest) {
    try {
      const response = await getToken(credentials.username, credentials.password)
      TokenStorage.setToken(response.token)
      const newUserInfo = { id: response.user_id, fullName: response.full_name }
      UserStorage.setUserInfo(newUserInfo)
      userInfo.value = newUserInfo
      isAuthenticated.value = true
      fullName.value = response.full_name
      userId.value = response.user_id
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
    UserStorage.clearUserInfo()
    userInfo.value = null
    isAuthenticated.value = false
    fullName.value = ''
    userId.value = null
    await router.push({ name: 'login' })
  }

  return {
    isAuthenticated,
    fullName,
    userId,
    login,
    logout,
  }
})
