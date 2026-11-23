/**
 * Resolves the storefront URL dynamically based on environment.
 * In production/hosted mode (Vercel), routes to relative '/' on the same domain.
 * In local development, routes to 'http://localhost:5173'.
 */

export function getStorefrontUrl(path = '') {
  const cleanPath = path ? (path.startsWith('/') ? path : `/${path}`) : '/'
  if (import.meta.env.VITE_STOREFRONT_URL) {
    const base = import.meta.env.VITE_STOREFRONT_URL.replace(/\/$/, '')
    return `${base}${cleanPath}`
  }
  if (
    import.meta.env.VITE_HOSTED_DEPLOYMENT === 'true' ||
    (typeof window !== 'undefined' &&
      window.location.hostname !== 'localhost' &&
      window.location.hostname !== '127.0.0.1')
  ) {
    return cleanPath
  }
  return `http://localhost:5173${cleanPath}`
}
