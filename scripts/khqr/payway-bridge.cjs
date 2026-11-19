// Local ABA PayWay link adapter. It handles only the configured payment page.
const { chromium } = require('playwright')

const paywayHosts = new Set(['link.payway.com.kh', 'checkout.payway.com.kh', 'checkout-sandbox.payway.com.kh'])
const emit = data => process.stdout.write(JSON.stringify(data) + '\n')

function trustedUrl(value) {
  const url = new URL(value)
  return url.protocol === 'https:' && !url.username && !url.password && !url.port && paywayHosts.has(url.hostname)
}

async function main() {
  const [amount, orderNumber] = process.argv.slice(2)
  const url = process.env.ABA_PAYWAY_URL
  if (!url || !trustedUrl(url) || !/^\d+\.\d{2}$/.test(amount) || Number(amount) <= 0 || !orderNumber) {
    throw new Error('The local bridge requires a valid PayWay link and order.')
  }

  const browser = await chromium.launch({ channel: 'chrome', headless: true })
  try {
    const page = await browser.newPage()
    let qr
    let clientId
    let approvalClientId
    let merchantName
    await page.route('**/*', route => {
      const request = route.request()
      return request.isNavigationRequest() && !trustedUrl(request.url())
        ? route.abort()
        : route.continue()
    })

    page.on('response', async response => {
      if (!response.ok() || !trustedUrl(response.url())) return
      try {
        const payload = await response.json()
        const candidate = payload.qr_string || payload.download_qr
        if (typeof candidate === 'string' && candidate.startsWith('000201')) {
          qr = candidate
          clientId = payload.client_id || clientId
          merchantName = payload.transaction_summary?.merchant?.company
        }
        if (new URL(response.url()).pathname.endsWith('/check-payment-status')) {
          const checkedId = response.request().postDataJSON()?.client_id
          clientId ||= checkedId
          if (checkedId && payload.data?.action === 'approved') approvalClientId = checkedId
        }
      } catch {
        // Ignore responses outside the PayWay JSON contract.
      }
    })

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 })
    await page.locator('#txt_amount').fill(amount, { timeout: 5000 })
    await page.locator('button.st-button').click({ timeout: 5000 })
    const qrDeadline = Date.now() + 8000
    while ((!qr || !clientId) && Date.now() < qrDeadline) {
      if (!qr && trustedUrl(page.url())) {
        const candidate = await page.evaluate(() => document.querySelector('div.khqr-content div[value]')?.getAttribute('value'))
        if (typeof candidate === 'string' && candidate.startsWith('000201')) qr = candidate
      }
      await page.waitForTimeout(250)
    }
    if (!qr || !clientId) throw new Error('No matching QR and session ID were returned.')
    const sessionId = String(clientId)
    emit({ event: 'qr_ready', qr_string: qr, client_id: sessionId, order_number: orderNumber, merchant_name: merchantName })

    const paymentDeadline = Date.now() + 300000
    while (Date.now() < paymentDeadline) {
      if (approvalClientId && String(approvalClientId) === sessionId) {
        emit({ event: 'paid', client_id: sessionId, order_number: orderNumber })
        return
      }
      await page.waitForTimeout(1000)
    }
    emit({ event: 'timeout' })
  } finally {
    await browser.close()
  }
}

main().catch(() => {
  emit({ event: 'error' })
  process.exitCode = 1
})
