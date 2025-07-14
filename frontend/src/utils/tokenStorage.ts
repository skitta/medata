import CryptoJS from 'crypto-js'

const SECRET_KEY = 'medata-token-encryption-key-2024'
const TOKEN_STORAGE_KEY = 'mt_secure_token'

interface StoredToken {
  encryptedToken: string
  expiresAt: number
}

export class TokenStorage {
  /**
   * Encrypts and stores the token object in localStorage.
   * @param token The raw token string to store.
   * @param expiresInHours The number of hours until the token expires. Defaults to 24.
   */
  static setToken(token: string, expiresInHours: number = 24): void {
    try {
      const expiresAt = Date.now() + expiresInHours * 60 * 60 * 1000
      const encryptedToken = CryptoJS.AES.encrypt(token, SECRET_KEY).toString()
      const tokenData: StoredToken = { encryptedToken, expiresAt }
      localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokenData))
    } catch (error) {
      console.error('Error storing token:', error)
    }
  }

  /**
   * Retrieves and decrypts the token from localStorage.
   * Returns null if the token is not found, expired, or if decryption fails.
   * @returns The decrypted token string, or null.
   */
  static getToken(): string | null {
    try {
      const tokenDataString = localStorage.getItem(TOKEN_STORAGE_KEY)
      if (!tokenDataString) return null

      const tokenData: StoredToken = JSON.parse(tokenDataString)

      if (Date.now() > tokenData.expiresAt) {
        this.clearToken()
        return null
      }

      const bytes = CryptoJS.AES.decrypt(tokenData.encryptedToken, SECRET_KEY)
      const decryptedToken = bytes.toString(CryptoJS.enc.Utf8)

      return decryptedToken || null
    } catch (error) {
      console.error('Error retrieving token:', error)
      this.clearToken()
      return null
    }
  }

  /**
   * Checks if a valid, non-expired token exists.
   * @returns True if the token is valid, false otherwise.
   */
  static isTokenValid(): boolean {
    return this.getToken() !== null
  }

  private static getStoredToken(): StoredToken | null {
    try {
      const tokenDataString = localStorage.getItem(TOKEN_STORAGE_KEY)
      return tokenDataString ? JSON.parse(tokenDataString) : null
    } catch {
      return null
    }
  }

  /**
   * Checks if the token will expire within a specified time frame.
   * @param minutes The time frame in minutes to check for expiration. Defaults to 5.
   * @returns True if the token is expiring soon, false otherwise.
   */
  static isTokenExpiringSoon(minutes: number = 5): boolean {
    const tokenData = this.getStoredToken()
    if (!tokenData) return false

    const threshold = Date.now() + minutes * 60 * 1000
    return tokenData.expiresAt <= threshold
  }

  /**
   * Gets the remaining time until the token expires.
   * @returns The remaining time in milliseconds, or 0 if not applicable.
   */
  static getTokenTimeRemaining(): number {
    const tokenData = this.getStoredToken()
    if (!tokenData) return 0

    const remaining = tokenData.expiresAt - Date.now()
    return Math.max(0, remaining)
  }

  /**
   * Removes the token from localStorage.
   */
  static clearToken(): void {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
  }

  /**
   * Refreshes the token's expiration time.
   * @param expiresInHours The number of hours to extend the token's validity. Defaults to 24.
   * @returns True if the token was refreshed successfully, false otherwise.
   */
  static refreshTokenExpiry(expiresInHours: number = 24): boolean {
    try {
      const tokenData = this.getStoredToken()
      if (!tokenData) return false

      tokenData.expiresAt = Date.now() + expiresInHours * 60 * 60 * 1000
      localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokenData))
      return true
    } catch {
      return false
    }
  }
}
