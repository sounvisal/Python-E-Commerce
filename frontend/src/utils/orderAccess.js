export function rememberOrderAccess(order) {
  if (order?.access_token) sessionStorage.setItem(`lumea_order_access_${order.order_number}`, order.access_token)
}
export function orderRequest(orderNumber) {
  const token = sessionStorage.getItem(`lumea_order_access_${orderNumber}`)
  return token ? { headers: { 'X-Order-Token': token } } : {}
}
export function privateStorageKey(name) {
  try {
    const user = JSON.parse(sessionStorage.getItem('lumea_auth_user') || localStorage.getItem('lumea_auth_user') || 'null')
    return `lumea_${name}_${user?.id || 'guest'}`
  } catch { return `lumea_${name}_guest` }
}
