const USER_KEY = 'mt_user'

export interface UserInfo {
  id: number
  fullName: string
}

export class UserStorage {
  /**
   * Stores the user info in localStorage.
   * @param userInfo The user info object to store.
   */
  static setUserInfo(userInfo: UserInfo): void {
    try {
      localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
    } catch (error) {
      console.error('Error storing user info:', error)
    }
  }

  /**
   * Retrieves the user info from localStorage.
   * @returns The user info object, or null.
   */
  static getUserInfo(): UserInfo | null {
    try {
      const userInfoString = localStorage.getItem(USER_KEY)
      if (!userInfoString) return null
      return JSON.parse(userInfoString)
    } catch (error) {
      console.error('Error retrieving user info:', error)
      return null
    }
  }

  /**
   * Removes the user info from localStorage.
   */
  static clearUserInfo(): void {
    localStorage.removeItem(USER_KEY)
  }
}
