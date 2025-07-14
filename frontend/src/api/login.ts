import { authApi } from '@/plugins/axios'
import { TokenResponse } from '@/types/api'


export async function getToken(username: string, password: string): Promise<TokenResponse> {
  try {
    const response = await authApi.post<TokenResponse>('token-auth/', {
      username,
      password,
    })
    return response.data
  } catch (error) {
    // The error will be caught by the calling function in LoginView.vue
    throw error
  }
}
