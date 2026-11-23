# Deploy Luméa E-Commerce: Vercel (Frontend) + Render (Backend)

This is the complete, beginner-friendly guide to deploying the **Luméa Skincare Atelier** with:
- **Frontend & Admin**: Hosted on **Vercel** (Storefront at `/`, Admin Atelier at `/atelier/`)
- **Backend API**: Hosted on **Render** (Python FastAPI ASGI service)
- **Database**: **Neon PostgreSQL** (Free tier, zero maintenance) or fallback SQLite

---

## 🏗️ Architecture at a Glance

```mermaid
graph LR
    User["Client Browser"] -->|Visits / and /atelier| Vercel["Vercel Global Edge<br/>(Storefront + Admin)"]
    Vercel -->|Proxies /api, /images/uploads, /videos| Render["Render Web Service<br/>(Python FastAPI)"]
    Render --> Neon[("Neon PostgreSQL<br/>(Serverless Database)")]
```

### Why this setup is ideal:
1. **Zero CORS Issues**: Vercel serves the HTML/JS and reverse-proxies `/api` requests to Render. The browser talks only to your Vercel domain (`https://your-site.vercel.app/api/...`), so requests are treated as same-origin.
2. **Instant Global Delivery**: Vercel delivers static Vue assets with zero latency across worldwide edge servers.
3. **Clean Separation**: Render focuses entirely on the Python API, database models, background order sweeps, and payment verification.

---

## 📋 Prerequisites Checklist

Before you begin, ensure you have:
- [x] A **GitHub account** with the Luméa repository pushed.
- [x] A free **[Render.com](https://render.com)** account.
- [x] A free **[Vercel.com](https://vercel.com)** account.
- [x] *(Recommended)* A free **[Neon.tech](https://neon.tech)** PostgreSQL account (takes 60 seconds).

---

## 🗄️ Step 1: Create Your Neon PostgreSQL Database (~2 Mins)

1. Go to **[neon.tech](https://neon.tech)** and sign in.
2. Click **Create Project**:
   - **Name**: `lumea-db`
   - **Region**: Choose the region closest to you (e.g. `Singapore ap-southeast-1` or `US East`).
3. On the project dashboard under **Connection Details**:
   - Ensure the **Connection pooling** toggle is **OFF** (use the Direct connection).
   - Copy your connection string. It looks like:
     ```text
     postgresql://neondb_owner:npg_xxxxxx@ep-xxxxxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
     ```
4. Save this string for Step 2.

> **💡 Quick Demo Note**: If you don't want to create a Neon account right now, you can skip this step! Luméa automatically falls back to an embedded SQLite database if `DATABASE_URL` is omitted.

---

## 🐍 Step 2: Deploy the FastAPI Backend to Render (~3 Mins)

You can deploy on Render using either **Option A (Automatic Blueprint)** or **Option B (Manual Setup)**.

### Option A: Automatic Blueprint (Recommended)
1. Go to **[dashboard.render.com](https://dashboard.render.com)**.
2. Click **New +** -> **Blueprint**.
3. Connect your GitHub repository (`Python-E-Commerce`).
4. Render will read [`render.yaml`](file:///d:/lumea/render.yaml) automatically.
5. In the parameter prompt:
   - Paste your Neon connection string into `DATABASE_URL`.
   - Render automatically generates a secure 256-bit `SECRET_KEY`.
6. Click **Apply**. Render will install dependencies and start Uvicorn.

---

### Option B: Manual Web Service Setup (Step-by-Step)
1. Go to **[dashboard.render.com](https://dashboard.render.com)**.
2. Click **New +** -> **Web Service**.
3. Select your GitHub repository.
4. Fill in the basic settings:
   - **Name**: `lumea-backend` *(or your preferred name)*
   - **Region**: Same as Neon *(e.g. Singapore)*
   - **Branch**: `main`
   - **Root Directory**: *(leave blank — repository root)*
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     python -m pip install -r python-backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     python -m uvicorn --app-dir python-backend app.main:app --host 0.0.0.0 --port "$PORT" --workers 1 --no-access-log
     ```
   - **Instance Type**: `Free`
5. Scroll down to **Environment Variables** and add:

   | Key | Value | Notes |
   | :--- | :--- | :--- |
   | `PRODUCTION` | `true` | Enables production security & headers |
   | `SERVE_BUILT_APPS` | `false` | Backend runs API-only (Vercel serves frontend) |
   | `DATABASE_URL` | *`postgresql://neondb_owner:...`* | Your Neon string (or leave empty for SQLite) |
   | `SECRET_KEY` | *(Click "Generate" or enter 32+ random characters)* | Cryptographic JWT signing key |
   | `ADMIN_EMAIL` | `admin@lumea.com` | Atelier administrator login email |
   | `ADMIN_PASSWORD` | `password123` | Atelier administrator login password |
   | `ENABLE_DEMO_PAYMENTS` | `false` | Keeps live security enabled |

6. Scroll down to **Advanced** -> set **Health Check Path** to `/api/live`.
7. Click **Deploy Web Service**.

### 🔍 Verify Backend Deployment:
1. Wait until Render displays **Deploy live 🎉**.
2. Copy your Render HTTPS origin (e.g., `https://lumea-backend.onrender.com`).
3. Open `https://lumea-backend.onrender.com/api/health` in your browser.
   - You should see: `{"status": "healthy", "service": "Luméa E-Commerce API", "database": "connected"}`.
4. Keep this Render URL handy for Step 3.

---

## ⚡ Step 3: Deploy the Frontend to Vercel (~2 Mins)

1. Go to **[vercel.com/new](https://vercel.com/new)**.
2. Find your `Python-E-Commerce` repository and click **Import**.
3. In the **Configure Project** screen:
   - **Project Name**: `lumea` *(or any name you prefer)*
   - **Framework Preset**: Select **Other**
   - **Root Directory**: `./` *(leave default repository root)*
4. Expand the **Environment Variables** section and add:
   - **Name**: `RENDER_API_ORIGIN`
   - **Value**: `https://lumea-backend.onrender.com` *(Replace with your actual Render URL from Step 2. Do **NOT** add a trailing slash).*
5. Click **Deploy**.

### What Vercel does automatically:
- Installs dependencies for both `frontend` and `admin`.
- Runs [`scripts/build-vercel.mjs`](file:///d:/lumea/scripts/build-vercel.mjs) to compile the Storefront to `/` and Admin Atelier to `/atelier/`.
- Applies [`vercel.ts`](file:///d:/lumea/vercel.ts) routes to forward `/api/*`, `/images/uploads/*`, and `/videos/*` to Render, while routing all SPA navigation cleanly without 404s.

---

## ✅ Step 4: Verification & Grading Checklist

Once Vercel completes deployment, test your live store:

| Test Item | URL / Path to Open | Expected Behavior |
| :--- | :--- | :--- |
| **Storefront Homepage** | `https://your-site.vercel.app/` | Loads luxury hero banner, bestsellers, featured skincare products |
| **Catalog & Filtering** | `https://your-site.vercel.app/shop` | Category badges, price slider, and sorting work smoothly |
| **Product Detail** | Click any product (e.g. *SK-II Essence*) | Gallery, dermatological accordions, ingredients, and video reels render |
| **Sensory Video Reels** | Bottom of Product Detail page | Plays vertical UGC video demonstration with audio toggle |
| **Cart & Slide-out Bag** | Click "Add to Bag" | Counter badge increments, slide-out drawer opens smoothly |
| **Cash on Delivery Checkout**| `https://your-site.vercel.app/checkout` | Select Cash on Delivery -> Place Order -> Confirmed `LUM-XXXXXX` invoice |
| **Bakong KHQR Modal** | Checkout -> Select Bakong KHQR | Displays official NBC crimson banner, dual USD/KHR total, dynamic QR code |
| **Admin Atelier Console** | `https://your-site.vercel.app/atelier/` | Directs to Atelier login (`admin@lumea.com` / `password123`) |
| **Admin Dashboard** | `https://your-site.vercel.app/atelier/dashboard` | Displays KPI cards, revenue metrics, donut charts, and recent orders |
| **Admin Order Lookup** | `https://your-site.vercel.app/atelier/orders` | The order placed in Storefront appears with full timeline & invoice |
| **Deep Link Refresh** | Refresh `/shop` or `/atelier/dashboard` | Reloads properly without a Vercel 404 error |
| **API Health Check** | `https://your-site.vercel.app/api/health` | Proxies to Render and returns `"database": "connected"` |

---

## 💳 Payment Gateway Details (KHQR & ABA PayWay)

- **Cash on Delivery (COD)**: Available immediately out-of-the-box.
- **Bakong KHQR**:
  - The storefront dynamically generates standard NBC-compliant EMVCo TLV QR payloads with dual currency calculation (e.g. `$99.00 ≈ 405,900 KHR`).
  - When live ABA PayWay credentials are added on Render (`PAYWAY_MERCHANT_ID`, `PAYWAY_API_KEY`), real ABA bank transfers are signed, verified, and settled automatically.
  - Vercel reverse-proxies payment polling, so customer checkout needs no special network configuration.

---

## 🛠️ Frequently Asked Questions & Troubleshooting

### 1. Why does my first API request take ~45 seconds on Render?
Render's free tier spins down idle web services after 15 minutes of inactivity. When a customer visits your site after an idle period, Render takes 45–60 seconds to wake the container. Subsequent requests are fast and instant.

### 2. Vercel build failed with: `Set RENDER_API_ORIGIN to the HTTPS origin...`
This means the `RENDER_API_ORIGIN` environment variable was omitted or formatted incorrectly.
1. Open your Vercel Project Dashboard -> **Settings** -> **Environment Variables**.
2. Add `RENDER_API_ORIGIN` = `https://your-service.onrender.com` (ensure it starts with `https://` and has no trailing `/`).
3. Click **Deployments** -> **Redeploy**.

### 3. I get a `401 Unauthorized` when logging into Admin.
- If you specified `ADMIN_EMAIL` and `ADMIN_PASSWORD` in Render's environment variables, use those credentials.
- In demo/development environments, the default account is `admin@lumea.com` with password `password123`.

### 4. How do I test the split Vercel build locally before pushing?
You can build and test the exact Vercel static output locally:
```powershell
# 1. Build storefront to dist/ and admin to dist/atelier/
node scripts/build-vercel.mjs

# 2. Run the automated split verification test
node .browser-qa/check-split.mjs
```

---

## 🎓 Summary of Demo Credentials for Viva / Defense

- **Shopper Account**:
  - **Email**: `sreynich.chan@example.com`
  - **Password**: `password123`
  - **Role**: Customer (Luméa Radiant Gold VIP)
- **Atelier Administrator Account**:
  - **Email**: `admin@lumea.com`
  - **Password**: `password123`
  - **Role**: Administrator (Full Atelier Console Access at `/atelier/`)
