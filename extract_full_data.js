const { chromium } = require('playwright');
const fs = require('fs');
const https = require('https');
const QRCode = require('qrcode');

async function downloadImage(url, filepath) {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            if (response.statusCode === 200) {
                const fileStream = fs.createWriteStream(filepath);
                response.pipe(fileStream);
                fileStream.on('finish', () => {
                    fileStream.close();
                    resolve(filepath);
                });
            } else {
                reject(new Error(`Failed to download: ${response.statusCode}`));
            }
        }).on('error', reject);
    });
}

async function extractAndMonitor(url, amount) {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    
    let apiResponse = null;
    let paymentApproved = false;
    let receiptUrl = '';
    let paymentData = null;
    
    await context.route('**/*', (route) => {
        const resourceType = route.request().resourceType();
        if (['image', 'stylesheet', 'font', 'media'].includes(resourceType)) {
            route.abort();
        } else {
            route.continue();
        }
    });

    const page = await context.newPage();
    
    const client = await context.newCDPSession(page);
    await client.send('Network.enable');

    client.on('Network.responseReceived', async (params) => {
        const responseUrl = params.response.url;
        
        if (responseUrl.includes('payment') || responseUrl.includes('qr') || responseUrl.includes('aba')) {
            try {
                const response = await client.send('Network.getResponseBody', {
                    requestId: params.requestId
                });
                
                if (response.body) {
                    try {
                        const data = JSON.parse(response.body);
                        
                        if (data.qr_string || data.download_qr || data.step) {
                            apiResponse = data;
                        }
                        
                        if (data.data && data.data.action === 'approved') {
                            paymentApproved = true;
                            receiptUrl = data.data.download_receipt || '';
                            paymentData = data;
                        }
                    } catch (e) {}
                }
            } catch (e) {}
        }
    });

    try {
        await page.goto(url, { waitUntil: 'domcontentloaded' });
        await page.waitForSelector('#txt_amount', { timeout: 10000 });
        await page.fill('#txt_amount', amount.toString());
        await page.click('button.st-button');
        await page.waitForSelector('div.khqr-content div[value]', { timeout: 15000 });
        
        await page.waitForTimeout(3000);
        
        const qrRawData = await page.getAttribute('div.khqr-content div[value]', 'value');
        
        let qrImagePath = null;
        if (apiResponse && apiResponse.download_qr) {
            try {
                const timestamp = Date.now();
                qrImagePath = `qr_${timestamp}.png`;
                await downloadImage(apiResponse.download_qr, qrImagePath);
            } catch (e) {
                qrImagePath = null;
            }
        }
        
        const result = {
            success: true,
            qr_string: apiResponse?.qr_string || qrRawData,
            expire_in: apiResponse?.expire_in,
            expire_in_sec: apiResponse?.expire_in_sec,
            download_qr: apiResponse?.download_qr,
            qr_image_saved: qrImagePath,
            transaction_summary: apiResponse?.transaction_summary,
            payment_options: apiResponse?.payment_options,
            status: apiResponse?.status,
            client_id: apiResponse?.client_id
        };
        
        console.log(JSON.stringify(result, null, 2));
        
        console.log('');
        const qrAscii = await QRCode.toString(result.qr_string, { type: 'terminal', small: true });
        console.log(qrAscii);
        
        console.log('Checking payment...');
        
        const startTime = Date.now();
        const timeout = 300000;
        const interval = 2000;
        
        while (Date.now() - startTime < timeout) {
            if (paymentApproved) {
                console.log('Payment successful!');
                console.log('Receipt URL:', receiptUrl);
                await browser.close();
                return {
                    ...result,
                    payment: {
                        paid: true,
                        receipt_url: receiptUrl,
                        elapsed_time: (Date.now() - startTime) / 1000,
                        data: paymentData
                    }
                };
            }
            await new Promise(resolve => setTimeout(resolve, interval));
        }
        
        console.log('Timeout');
        await browser.close();
        return {
            ...result,
            payment: { paid: false, timeout: true }
        };
        
    } catch (error) {
        await browser.close();
        return {
            success: false,
            error: error.message
        };
    }
}

const args = process.argv.slice(2);
const url = args[0] || 'https://link.payway.com.kh/ABAPAYaC455755m';
const amount = parseFloat(args[1]) || 0.01;

extractAndMonitor(url, amount)
    .catch(err => {
        console.error('Error:', err.message);
        process.exit(1);
    });
