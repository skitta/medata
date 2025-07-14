import CryptoJS from 'crypto-js'

const SECRET_KEY = 'medata-token-encryption-key-2024'
const TOKEN_KEY = 'mt_token'
const EXPIRY_KEY = 'mt_expiry'

export interface SecureToken {
  token: string
  expiresAt: number
}

export class TokenStorage {
  /**
   * Encrypts and stores the token in sessionStorage.
   * @param token The token string to store.
   * @param expiresInHours The number of hours until the token expires. Defaults to 24.
   */
  static setToken(token: string, expiresInHours: number = 24): void {
    try {
      const expiresAt = Date.now() + expiresInHours * 60 * 60 * 1000
      const encryptedToken = CryptoJS.AES.encrypt(token, SECRET_KEY).toString()
      sessionStorage.setItem(TOKEN_KEY, encryptedToken)
      sessionStorage.setItem(EXPIRY_KEY, expiresAt.toString())
    } catch (error) {
      console.error('Error storing token:', error)
    }
  }

  /**
   * Retrieves and decrypts the token from sessionStorage.
   * Returns null if the token is not found, expired, or if decryption fails.
   * @returns The decrypted token string, or null.
   */
  static getToken(): string | null {
    try {
      const encryptedToken = sessionStorage.getItem(TOKEN_KEY)
      const expiry = sessionStorage.getItem(EXPIRY_KEY)

      if (!encryptedToken || !expiry) {
        return null
      }

      if (Date.now() > parseInt(expiry, 10)) {
        this.clearToken()
        return null
      }

      const bytes = CryptoJS.AES.decrypt(encryptedToken, SECRET_KEY)
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

  /**
   * Checks if the token will expire within a specified time frame.
   * @param minutes The time frame in minutes to check for expiration. Defaults to 5.
   * @returns True if the token is expiring soon, false otherwise.
   */
  static isTokenExpiringSoon(minutes: number = 5): boolean {
    try {
      const expiry = sessionStorage.getItem(EXPIRY_KEY)
      if (!expiry) return false

      const expiryTime = parseInt(expiry, 10)
      const threshold = Date.now() + minutes * 60 * 1000

      return expiryTime <= threshold
    } catch {
      return false
    }
  }

  /**
   * Gets the remaining time until the token expires.
   * @returns The remaining time in milliseconds, or 0 if not applicable.
   */
  static getTokenTimeRemaining(): number {
    try {
      const expiry = sessionStorage.getItem(EXPIRY_KEY)
      if (!expiry) return 0

      const remaining = parseInt(expiry, 10) - Date.now()
      return Math.max(0, remaining)
    } catch {
      return 0
    }
  }

  /**
   * Removes the token and its expiry from sessionStorage.
   */
  static clearToken(): void {
    sessionStorage.removeItem(TOKEN_KEY)
    sessionStorage.removeItem(EXPIRY_KEY)
  }

  /**
   * Refreshes the token's expiration time.
   * @param expiresInHours The number of hours to extend the token's validity. Defaults to 24.
   * @returns True if the token was refreshed successfully, false otherwise.
   */
  static refreshTokenExpiry(expiresInHours: number = 24): boolean {
    try {
      const encryptedToken = sessionStorage.getItem(TOKEN_KEY)
      if (!encryptedToken) return false

      // Re-set the token with a new expiry without re-encrypting
      const expiresAt = Date.now() + expiresInHours * 60 * 60 * 1000
      sessionStorage.setItem(EXPIRY_KEY, expiresAt.toString())
      return true
    } catch {
      return false
    }
  }
}
