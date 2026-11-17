const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const context = await browser.newContext({ viewport: { width: 1200, height: 950 } });
  const page = await context.newPage();

  await page.goto('http://localhost:5173/', { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => {
    const sampleItem = {
      id: 101,
      title: "Radiance Dew Essence",
      slug: "radiance-dew-essence",
      price: 23.90,
      image: "/images/products/product-1.jpg",
      quantity: 1,
      selectedVolume: "150ml"
    };
    localStorage.setItem('lumea_cart', JSON.stringify([sampleItem]));
  });

  console.log('Navigating to checkout...');
  await page.goto('http://localhost:5173/checkout', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  // Fill in form fields
  await page.fill('#cName', 'Sreynich Chan');
  await page.fill('#cEmail', 'sreynich.chan@example.com');
  await page.fill('#cPhone', '+855 12 345 678');
  await page.fill('#sAddress', '123 Norodom Boulevard, Sangkat Tonle Bassac');
  await page.selectOption('#sCity', 'Phnom Penh');

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

  console.log('Clicking #btn-authorize-order...');
  await page.click('#btn-authorize-order');
  await page.waitForTimeout(1000);

  const errorBanner = await page.$('.error-banner');
  if (errorBanner) {
    console.log('Server quote updated, clicking #btn-authorize-order again...');
    await page.click('#btn-authorize-order');
  }

  console.log('Waiting for .qr-canvas-element...');
  try {
    await page.waitForSelector('.qr-canvas-element', { timeout: 10000 });
    console.log('SUCCESS: .qr-canvas-element found!');
  } catch (e) {
    console.log('Timeout waiting for .qr-canvas-element. Current URL:', page.url());
    await page.screenshot({ path: 'checkout_debug.png' });
  }
  await page.waitForTimeout(1000);

  await page.screenshot({ path: 'khqr_new_design.png' });
  console.log('SUCCESS: Saved complete QR screenshot to khqr_new_design.png');

  await browser.close();
})().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
