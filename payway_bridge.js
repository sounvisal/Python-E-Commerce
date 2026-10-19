const puppeteer = require('puppeteer-core');

/**
 * Extracts live Bakong KHQR from ABA PayWay link.
 * Usage: node payway_bridge.js [amount] [url]
 */
async function fetchPaywayKHQR(amount = 0.01, url = 'https://link.payway.com.kh/ABAPAYaC455755m') {
  let browser = null;
  try {
    browser = await puppeteer.launch({
      executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });

    const page = await browser.newPage();
    
    let apiResponse = null;
    let clientId = null;
    let paymentApproved = false;
    let receiptUrl = '';

    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const type = req.resourceType();
      if (['image', 'media', 'font', 'stylesheet'].includes(type) && !req.url().includes('khqr')) {
        req.abort();
      } else {
        req.continue();
      }
    });

    page.on('response', async (res) => {
      const u = res.url();
      if (u.includes('list-payment-options') || u.includes('check-payment-status') || u.includes('payment/gateway')) {
        try {
          const body = await res.json();
          if (body.step || body.token || body.qr_string || body.download_qr) {
            apiResponse = body;
          }
          if (body.data && body.data.action === 'approved') {
            paymentApproved = true;
            receiptUrl = body.data.download_receipt || '';
          }
        } catch (e) {}
      }
    });

    page.on('request', (req) => {
      if (req.url().includes('check-payment-status')) {
        try {
          const postData = JSON.parse(req.postData() || '{}');
          if (postData.client_id) {
            clientId = postData.client_id;
          }
        } catch (e) {}
      }
    });

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForSelector('#txt_amount', { timeout: 15000 });
    
    // Clear and fill amount
    await page.click('#txt_amount', { clickCount: 3 });
    await page.type('#txt_amount', amount.toString());
    
    // Submit
    await page.click('button.st-button');
    
    // Wait for KHQR
    await page.waitForSelector('div.khqr-content div[value]', { timeout: 20000 });
    const qrString = await page.$eval('div.khqr-content div[value]', el => el.getAttribute('value'));

    // Wait a brief moment to capture clientId from check-payment-status
    for (let i = 0; i < 6; i++) {
      if (clientId) break;
      await new Promise(r => setTimeout(r, 500));
    }

    await browser.close();

    return {
      success: true,
      qr_string: qrString,
      client_id: clientId,
      amount: amount,
      currency: 'USD',
      merchant_name: 'SUON VISAL',
      source: 'live_aba_payway'
    };
  } catch (err) {
    if (browser) await browser.close();
    return {
      success: false,
      error: err.message
    };
  }
}

// Check live payment status directly via HTTP without opening a browser!
async function checkPaywayStatus(clientId, deviceId = 'r4PdITM507') {
  const https = require('https');
  const now = new Date();
  const reqTime = now.getFullYear().toString() + 
    String(now.getMonth() + 1).padStart(2, '0') + 
    String(now.getDate()).padStart(2, '0') + 
    String(now.getHours()).padStart(2, '0') + 
    String(now.getMinutes()).padStart(2, '0') + 
    String(now.getSeconds()).padStart(2, '0');

  // If clientId is provided, check with ABA API
  return new Promise((resolve) => {
    const postData = JSON.stringify({
      device_id: deviceId,
      request_time: reqTime,
      client_id: clientId
    });

    const req = https.request('https://pwapp.ababank.com/api/pw-app/v1/payment-link/check-payment-status', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
      },
      timeout: 5000
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.data && json.data.action === 'approved') {
            resolve({ approved: true, receipt: json.data.download_receipt || '', raw: json });
          } else {
            resolve({ approved: false, action: json.data?.action || 'pending', raw: json });
          }
        } catch (e) {
          resolve({ approved: false, error: 'parse_error' });
        }
      });
    });

    req.on('error', () => resolve({ approved: false, error: 'network_error' }));
    req.on('timeout', () => { req.destroy(); resolve({ approved: false, error: 'timeout' }); });
    req.write(postData);
    req.end();
  });
}

// CLI handler
const mode = process.argv[2] || 'generate';
if (mode === 'generate') {
  const amount = parseFloat(process.argv[3]) || 0.01;
  const url = process.argv[4] || 'https://link.payway.com.kh/ABAPAYaC455755m';
  fetchPaywayKHQR(amount, url).then(res => console.log(JSON.stringify(res)));
} else if (mode === 'check') {
  const clientId = process.argv[3];
  checkPaywayStatus(clientId).then(res => console.log(JSON.stringify(res)));
}

module.exports = { fetchPaywayKHQR, checkPaywayStatus };
