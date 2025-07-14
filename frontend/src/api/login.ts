import { authApi } from '@/plugins/axios'

export async function getToken(username: string, password: string): Promise<string> {
  try {
    const response = await authApi.post<{ token: string }>('token-auth/', {
      username,
      password,
    })
    return response.data.token
  } catch (error) {
    // The error will be caught by the calling function in LoginView.vue
    throw error
  }
}
