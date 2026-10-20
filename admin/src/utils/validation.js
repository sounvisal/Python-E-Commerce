/**
 * Product form validation
 * @param {Object} form - Product form data
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateProduct(form) {
  const errors = []

  // Required fields
  if (!form.name || !form.name.trim()) {
    errors.push('Product name is required')
  }
  if (form.name && form.name.length > 200) {
    errors.push('Product name must be 200 characters or less')
  }

  // SKU validation
  if (form.sku && !/^[A-Z0-9-]+$/i.test(form.sku)) {
    errors.push('SKU can only contain letters, numbers, and hyphens')
  }

  // Price validation
  if (form.price === null || form.price === undefined || form.price === '') {
    errors.push('Price is required')
  }
  if (Number(form.price) < 0) {
    errors.push('Price cannot be negative')
  }
  if (Number(form.price) > 999999) {
    errors.push('Price is too high (max: $999,999)')
  }

  // Stock validation
  if (form.stock === null || form.stock === undefined || form.stock === '') {
    errors.push('Stock quantity is required')
  }
  if (Number(form.stock) < 0) {
    errors.push('Stock cannot be negative')
  }
  if (!Number.isInteger(Number(form.stock))) {
    errors.push('Stock must be a whole number')
  }

  // Category validation
  if (!form.category_id) {
    errors.push('Category is required')
  }

  // Brand validation
  if (!form.brand || !form.brand.trim()) {
    errors.push('Brand is required')
  }

  // Description validation
  if (form.description && form.description.length > 5000) {
    errors.push('Description is too long (max: 5000 characters)')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Category form validation
 * @param {Object} form - Category form data
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateCategory(form) {
  const errors = []

  if (!form.name || !form.name.trim()) {
    errors.push('Category name is required')
  }
  if (form.name && form.name.length > 100) {
    errors.push('Category name must be 100 characters or less')
  }

  if (!form.slug || !form.slug.trim()) {
    errors.push('Slug is required')
  }
  if (form.slug && !/^[a-z0-9-]+$/.test(form.slug)) {
    errors.push('Slug can only contain lowercase letters, numbers, and hyphens')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Brand form validation
 * @param {Object} form - Brand form data
 * @returns {Object} { valid: boolean, errors: string[] }
 */
export function validateBrand(form) {
  const errors = []

  if (!form.name || !form.name.trim()) {
    errors.push('Brand name is required')
  }
  if (form.name && form.name.length > 100) {
    errors.push('Brand name must be 100 characters or less')
  }

  if (form.slug && !/^[a-z0-9-]+$/.test(form.slug)) {
    errors.push('Slug can only contain lowercase letters, numbers, and hyphens')
  }

  if (form.website && form.website.trim() && form.website !== 'https://' && !isValidUrl(form.website)) {
    errors.push('Website must be a valid URL')
  }

  if (form.country && form.country.length > 100) {
    errors.push('Country must be 100 characters or less')
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

/**
 * Email validation
 * @param {string} email
 * @returns {boolean}
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * URL validation
 * @param {string} url
 * @returns {boolean}
 */
export function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}
