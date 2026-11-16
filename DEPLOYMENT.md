# Deploy Luméa on Render & Neon PostgreSQL

This guide covers deploying the full Luméa E-Commerce Atelier (Vue 3 Storefront, Vue 3 Admin Atelier, and Python FastAPI backend) using **Render** (free web service) and **Neon** (serverless PostgreSQL free tier), with fully functional **Bakong KHQR** payment processing.

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

## 2. How KHQR Works on Hosted Deployment

The hosted Luméa system features NBC Bakong KHQR payment processing:
1. **Dynamic EMVCo TLV Generation**:
   - Generates compliant Dynamic Bakong KHQR payload with standard CCITT CRC16 checksum.
   - Renders in real-time on HTML5 canvas with the central Bakong currency emblem.
   - Dual-currency display: Order total in USD with live conversion to Cambodian Riel (KHR).
2. **Interactive Academic Defense / Demo Mode**:
   - `ENABLE_DEMO_PAYMENTS: "true"` is configured in `render.yaml`.
   - On the KHQR checkout modal, an instant clearance button is available:
     `⚡ Demo Mode: Simulate Instant Bank Approval`
   - Clicking this simulates instantaneous NBC Bakong clearance (`DEMO-BAKONG-...`), transitions the order to `Paid`, and opens the order confirmation invoice without needing to deduct real funds.
3. **Optional Real ABA PayWay Integration**:
   - To connect a live ABA PayWay merchant payment link, set the `ABA_PAYWAY_URL` environment variable in Render. If set, customer can click **Open ABA Pay Link** or scan directly via ABA Mobile.
4. **Merchant Account Customization**:
   - `BAKONG_MERCHANT_NAME`: Displays your atelier name on the banking screen (defaults to `LUMEA ATELIER`).
   - `BAKONG_ACCOUNT_ID`: Your NBC Bakong / ABA account ID (defaults to `000000000000000`).

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
     - `ENABLE_DEMO_PAYMENTS`: `"true"`
     - `BAKONG_MERCHANT_NAME`: `"LUMEA ATELIER"`
     - `BAKONG_ACCOUNT_ID`: `"000000000000000"`
4. **Click Apply**:
   - Render will build both Vue frontends (`npm run build`) and start the FastAPI ASGI server with Uvicorn.
   - On first startup, the backend automatically creates all database tables and seeds the full catalog into Neon.

---

## 4. Automatic Database Seeding & Pre-seeded Accounts

On the very first launch with a fresh Neon database, the system automatically:
- Creates all relational tables.
- Seeds all 8 skincare categories, 46 formulations, dynamic banners, quizzes, and articles.
- Synchronizes all PostgreSQL primary key sequences (`SELECT setval(...)`) to prevent ID collisions.

### Default Login Accounts for Evaluation & Grading:
- **Atelier Administrator**:
  - **Email**: `admin@lumea.com`
  - **Password**: `password123`
  - **Role**: `admin` (Full access to Admin Atelier at `/atelier/`)
- **VIP Customer**:
  - **Email**: `sreynich.chan@example.com`
  - **Password**: `password123`
  - **Role**: `customer` | **Tier**: `Luméa Radiant Gold` (320 reward points)

---

## 5. Verifying the Deployment

Once Render finishes deploying:
1. **Storefront**: Open `https://<your-service>.onrender.com/`
2. **Admin Console**: Open `https://<your-service>.onrender.com/atelier/`
3. **Health Check**: Open `https://<your-service>.onrender.com/api/health` -> verify `"database": "connected"`
4. **Interactive Swagger Docs**: Open `https://<your-service>.onrender.com/docs`
5. **Test KHQR Checkout**:
   - Add any product to the shopping bag.
   - Proceed to Checkout -> select **Bakong KHQR** as payment method.
   - Confirm order -> the authentic KHQR modal appears with QR canvas, timer, and KHR conversion.
   - Click `⚡ Demo Mode: Simulate Instant Bank Approval` -> order confirms immediately as Paid!

---

## 6. Free Tier Notes

- **Render Inactivity**: Render free instances spin down after 15 minutes of inactivity. The first visit after spin-down takes ~45-60 seconds to wake up.
- **Neon Serverless Pooling**: Neon automatically sleeps idle compute after 5 minutes. Luméa's connection engine uses `pool_pre_ping=True` and `pool_recycle=300`, so queries wake Neon seamlessly.
