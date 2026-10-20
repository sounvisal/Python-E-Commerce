/**
 * Safely parse JSON from localStorage
 * @param {string} key - localStorage key
 * @param {any} fallback - Default value if parsing fails
 * @returns {any} Parsed value or fallback
 */
export function safeGetJSON(key, fallback = null) {
  try {
    const item = localStorage.getItem(key)
    if (!item) return fallback
    return JSON.parse(item)
  } catch (e) {
    console.error(`Failed to parse localStorage key "${key}":`, e)
    return fallback
  }
}

/**
 * Safely stringify and save to localStorage
 * @param {string} key - localStorage key
 * @param {any} value - Value to save
 * @returns {boolean} Success status
 */
export function safeSetJSON(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value))
    return true
  } catch (e) {
    console.error(`Failed to save to localStorage key "${key}":`, e)
    return false
  }
}

/**
 * Safely remove from localStorage
 * @param {string} key - localStorage key
 */
export function safeRemove(key) {
  try {
    localStorage.removeItem(key)
  } catch (e) {
    console.error(`Failed to remove localStorage key "${key}":`, e)
  }
}
