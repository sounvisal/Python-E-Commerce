import { test, beforeEach, after } from 'node:test'
import assert from 'node:assert/strict'
import { build } from 'esbuild'
import { writeFile, unlink } from 'node:fs/promises'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { resolve } from 'node:path'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

function storage() {
  const state = {}
  Object.defineProperties(state, {
    getItem: { value(key) { return Object.hasOwn(this, key) ? this[key] : null } },
    setItem: { value(key, value) { this[key] = String(value) } },
    removeItem: { value(key) { delete this[key] } },
  })
  return state
}
globalThis.localStorage = storage()
globalThis.sessionStorage = storage()
const root = fileURLToPath(new URL('..', import.meta.url))
const output = resolve(root, '.flow-test-bundle.mjs')
const bundle = await build({ stdin: { contents: `
export { useAuthStore } from '@/stores/auth'
export { useOrdersStore } from '@/stores/orders'
export { useProductStore } from '@/stores/products'
export { useQuizStore } from '@/stores/quiz'
export { useCartStore } from '@/stores/cart'
export { useJournalStore } from '@/stores/journal'
export { useWishlistStore } from '@/stores/wishlist'
`, resolveDir: root }, alias: { '@': resolve(root, 'src') }, bundle: true, format: 'esm', platform: 'node', external: ['vue', 'pinia', 'axios'], write: false })
await writeFile(output, bundle.outputFiles[0].text)
const stores = await import(pathToFileURL(output).href)
after(async () => { await unlink(output) })
let requests
let handler
beforeEach(() => {
  for (const s of [localStorage, sessionStorage]) for (const key of Object.keys(s)) s.removeItem(key)
  setActivePinia(createPinia())
  delete axios.defaults.headers.common.Authorization
  requests = []
  handler = () => { throw new Error('Unexpected request') }
  axios.defaults.adapter = async config => {
    requests.push(config)
    return { data: await handler(config), status: 200, statusText: 'OK', headers: {}, config }
  }
})
const user = (id = 1) => ({ id, name: `User ${id}`, email: `user${id}@example.com`, role: 'customer', reward_points: 0, profile_data: {} })
const authResponse = (id = 1) => ({ status: 'success', data: { access_token: `real-test-token-${id}`, user: user(id) } })

test('server failure never creates a demo login or registration session', async () => {
  const auth = stores.useAuthStore()
  assert.equal(await auth.login({email:'a@example.com',password:'test'}), false)
  assert.equal(await auth.register({name:'A User',email:'a@example.com',password:'test'}), false)
  assert.equal(auth.isAuthenticated, false)
  assert.equal(auth.token, null)
})
test('Remember me unchecked persists only to the current browser session', async () => {
  handler = () => authResponse()
  const auth = stores.useAuthStore()
  assert.equal(await auth.login({ email:'user1@example.com',password:'test',remember:false }), true)
  assert.equal(localStorage.getItem('lumea_auth_token'), null)
  assert.equal(sessionStorage.getItem('lumea_auth_token'), 'real-test-token-1')
  assert.equal(await auth.ensureSession(), true)
  assert.deepEqual(auth.user.addresses, [])
  assert.deepEqual(auth.user.paymentMethods, [])
})
test('logout clears in-memory purchases and guest access tokens', async () => {
  handler = () => authResponse()
  const auth=stores.useAuthStore()
  await auth.login({email:'user1@example.com',password:'test'})
  stores.useOrdersStore().orders=[{orderNumber:'private'}]
  sessionStorage.setItem('lumea_order_access_private','secret')
  auth.logout(false)
  assert.deepEqual(stores.useOrdersStore().orders,[])
  assert.equal(sessionStorage.getItem('lumea_order_access_private'),null)
})
test('account switches load only that accounts skin profile and diary', async () => {
  const auth=stores.useAuthStore()
  const quiz=stores.useQuizStore()
  const journal=stores.useJournalStore()
  handler=()=>authResponse(1)
  await auth.login({email:'user1@example.com',password:'test'})
  quiz.setAnswer('skinType','Dry')
  journal.addEntry({title:'Private diary',notes:'First user'})
  handler=()=>authResponse(2)
  await auth.login({email:'user2@example.com',password:'test'})
  assert.equal(quiz.answers.skinType,'')
  assert.deepEqual(journal.entries,[])
  handler=()=>authResponse(1)
  await auth.login({email:'user1@example.com',password:'test'})
  assert.equal(quiz.answers.skinType,'Dry')
  assert.equal(journal.entries[0].title,'Private diary')
})
test('profile save failure does not overwrite the displayed profile', async () => {
  handler=()=>authResponse()
  const auth=stores.useAuthStore()
  await auth.login({email:'user1@example.com',password:'test'})
  handler=()=>{ throw new Error('Offline') }
  assert.equal(await auth.updateProfile({name:'Unsaved name'}),false)
  assert.equal(auth.user.name,'User 1')
})
test('catalog fetch replaces fixture state and preserves empty server results', async () => {
  const products=stores.useProductStore()
  assert.deepEqual(products.allCatalogProducts,[])
  handler=()=>({data:[{id:55,name:'Live product',is_featured:true}]})
  await products.fetchProducts()
  assert.equal(products.allCatalogProducts[0].id,55)
  handler=()=>({data:[]})
  await products.fetchProducts()
  assert.deepEqual(products.allCatalogProducts,[])
})
test('missing order and failed cancellation do not invent local success', async () => {
  const orders=stores.useOrdersStore()
  assert.equal(orders.getOrderById('missing'),null)
  orders.orders=[{orderNumber:'existing',status:'Confirmed'}]
  assert.equal(await orders.cancelOrder('existing'),false)
  assert.equal(orders.orders[0].status,'Confirmed')
  assert.equal(await orders.fetchOrderByNumber('missing'),null)
})
test('promo application uses persisted backend rules instead of parsing digits', async () => {
  const cart=stores.useCartStore()
  handler=config=> { assert.equal(config.url,'/api/promotions/validate/SUMMER25'); return {code:'SUMMER25',rate:0.25} }
  assert.equal((await cart.applyPromoCode('summer25')).success,true)
  assert.equal(cart.discountRate,0.25)
})
