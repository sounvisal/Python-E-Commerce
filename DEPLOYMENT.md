# Deploy Luméa on Render & Neon PostgreSQL

This guide covers deploying the full Luméa E-Commerce Atelier (Vue 3 Storefront, Vue 3 Admin Atelier, and Python FastAPI backend) using **Render** (free web service) and **Neon** (serverless PostgreSQL free tier), with **Bakong KHQR** available after ABA PayWay merchant configuration.

---

## 1. Setup Neon Serverless PostgreSQL Database

1. **Sign up / Log in to Neon**:
   - Go to [neon.tech](https://neon.tech) and create a free account.
2. **Create a New Project**:
   - Project Name: `lumea-db` (or any preferred name).
   - Region: Choose **Singapore (ap-southeast-1)** or the region closest to your users / Render region.
   - Click **Create Project**.
3. **Get Direct Connection String**:
   - In your Neon project dashboard, go to the **Connect** or **Dashboard** tab.
   - Under *Connection Details*, ensure **Connection pooling** toggle is **OFF** (use the Direct connection string `ep-...` rather than `-pooler`). The Luméa backend manages its own internal connection pool (`pool_size=5, max_overflow=5, pool_recycle=300`).
   - Select **SQLAlchemy** or **Connection string**.
   - The connection string looks like:
     ```text
     postgresql://neondb_owner:npg_xxxxxx@ep-xxxxxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
     ```
   - Copy this string (keep it safe and private).

---

## 2. KHQR on Render and local development

The storefront uses the server-calculated order total. The hosted backend requests a signed QR from ABA PayWay and verifies the transaction against PayWay before marking the order paid. Neon holds the order, stock reservation, and payment status. Render offers cash on delivery until KHQR is configured.

In Render's **Environment** settings add the live ABA-issued `PAYWAY_MERCHANT_ID` and `PAYWAY_API_KEY`. Keep `PAYWAY_ENVIRONMENT=live` and `ENABLE_DEMO_PAYMENTS=false`. The callback uses Render's public HTTPS origin. Set `PAYWAY_PUBLIC_URL` to the HTTPS origin of your custom domain when ABA expects that domain. Ask ABA to confirm the merchant, callback URL, and any allowlisting requirements for your service before enabling live payments. Run a sandbox checkout from a public HTTPS staging origin first. [ABA QR API](https://developer.payway.com.kh/folder-3158158) · [ABA endpoints](https://developer.payway.com.kh/api-endpoints-984508m0)

For local development, the tracked `scripts/khqr/payway-bridge.cjs` uses the configured `ABA_PAYWAY_URL` with Playwright and installed Chrome. Set the link in the backend's ignored local environment file and install the root npm dependencies. This adapter checks the QR amount and currency and watches the matching payment session. Render uses the signed merchant API. Local administrator simulation is available only when explicitly enabled and no PayWay integration is configured.

A cancelled or expired order releases reserved stock. A verified payment received later goes to **Payment Review** for staff reconciliation.

---

## 3. Deploy to Render via Blueprint

1. **Push Changes to GitHub**:
   - Commit and push your code and `render.yaml` to your GitHub repository.
2. **Create Render Web Service**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** -> **Blueprint**.
   - Connect your GitHub repository.
   - Select your deployment branch.
   - Choose the **Free** tier.
3. **Provide Environment Variables**:
   - When prompted for `DATABASE_URL`, paste your Neon direct connection string (with `?sslmode=require`).
   - Render automatically generates a cryptographically secure 256-bit `SECRET_KEY`.
   - Ensure the following environment variables are present (pre-configured in `render.yaml`):
     - `PRODUCTION`: `"true"`
     - `SERVE_BUILT_APPS`: `"true"`
     - `VITE_HOSTED_DEPLOYMENT`: `"true"`
     - `ENABLE_DEMO_PAYMENTS`: `"false"`
     - `PAYWAY_ENVIRONMENT`: `live`
4. **Click Apply**:
   - Render will build both Vue frontends (`npm run build`) and start the FastAPI ASGI server with Uvicorn.
   - On first startup, the backend automatically creates all database tables and seeds the full catalog into Neon.

---

## 4. Production launch prerequisite

The current startup seeder creates evaluation accounts with known passwords and inserts a sample order. Before public launch, restrict these fixtures to local development, provision a unique administrator credential, and review any database already initialized by this seeder.

---

## 5. Verifying the Deployment

Once Render finishes deploying:
1. **Storefront**: Open `https://<your-service>.onrender.com/`
2. **Admin Console**: Open `https://<your-service>.onrender.com/atelier/`
3. **Health Check**: Open `https://<your-service>.onrender.com/api/health` -> verify `"database": "connected"`
4. Place a cash-on-delivery order and verify its total, receipt, and appearance in Admin.
5. In an ABA sandbox environment, select KHQR and verify that scanning the QR settles the stored order, updates Admin, and leaves the order in Payment Review if payment arrives after cancellation. Verify the same flow with ABA before accepting public payments.

---

## 6. Free Tier Notes

- **Render Inactivity**: Render free instances spin down after 15 minutes of inactivity. The first visit after spin-down takes ~45-60 seconds to wake up.
- **Neon Serverless Pooling**: Neon automatically sleeps idle compute after 5 minutes. Luméa's connection engine uses `pool_pre_ping=True` and `pool_recycle=300`, so queries wake Neon seamlessly.
