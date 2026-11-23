# LUMÉA — Contemporary Skincare & Beauty Atelier E-Commerce Platform

> A full-stack, enterprise-grade e-commerce application featuring a **Python 3.12 FastAPI REST API** backend, a **Vue 3 + Vite** storefront, and a dedicated **Vue 3 + Vite** Admin Atelier Console.

[![CI/CD Pipeline](https://github.com/sounvisal/Python-E-Commerce/actions/workflows/ci.yml/badge.svg)](https://github.com/sounvisal/Python-E-Commerce/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.5+-4FC08D?style=flat&logo=vue.js)](https://vuejs.org)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF?style=flat&logo=vite)](https://vitejs.dev)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat)](https://www.sqlalchemy.org)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python)](https://python.org)

---

## 🌟 1. System Architecture & Live Hosting

The Luméa system consists of three decoupled components communicating via RESTful JSON APIs:

```mermaid
graph LR
    subgraph Frontend Services (Vercel)
        Storefront["Vue 3 Storefront SPA<br/>(Port 5173 / Root Domain)"]
        AdminApp["Vue 3 Admin Atelier<br/>(Port 5174 /atelier/)"]
    end

    subgraph Backend Service (Render)
        FastAPI["Python FastAPI Server<br/>(Port 8000 /api/)<br/>ASGI / Uvicorn"]
        DB[("PostgreSQL / SQLite<br/>SQLAlchemy 2.0 ORM")]
    end

    Storefront -->|REST API| FastAPI
    AdminApp -->|REST API| FastAPI
    FastAPI --> DB
```

| Component | Technology Stack | Local Development | Hosted Production | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Storefront** | Vue 3, Pinia, Vue Router, Vite | `http://localhost:5173` | Vercel SPA (Root `/`) | Luxury bisque aesthetic (`#F5EFEB`, `#7A2E22`) |
| **Admin Console** | Vue 3, Pinia, Chart.js, Vite | `http://localhost:5174` | Vercel SPA (`/atelier/`) | Executive Atelier back-office console |
| **Backend API** | Python 3.12, FastAPI, SQLAlchemy 2.0 | `http://127.0.0.1:8000` | Render Web Service | Interactive Swagger at `/docs` |
| **Database** | SQLite 3 / PostgreSQL | `lumea.db` (File-based) | Managed PostgreSQL | Automated migrations and seeders |

For complete step-by-step production setup on Render and Vercel, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🎨 2. Feature Highlights & Module Inventory

### A. Storefront Experience (40 Completed Views & Regimens)
- **E-Commerce Catalog**: Filterable multi-attribute catalog (search, brand, category, skin type, concern, sort, and price bracket).
- **Video Texture Reviews & UGC Sensory Reels**: Vertical 9:16 video reels with skin profile tags, duration chips, and a 1-Click Quick-Buy "Add to Bag" reel player.
- **Dermatological Diagnostic Quiz**: 5-step diagnostic quiz mapping skin metrics to tailored morning and evening routine recommendations.
- **Bakong KHQR & Cash-on-Delivery (COD)**: Dynamic National Bank of Cambodia (NBC) Bakong EMVCo TLV QR generation with dual USD/KHR currency conversion and real-time bank clearance polling.
- **Customer Care & Regimen**: User account dashboard, order history invoice tracking, interactive return wizard (`/returns/request`), live return tracking timeline (`/returns/status/:id`), and private Skincare Journal diary.

### B. Admin Atelier Console (14 Specialized Modules)
1. **Executive Dashboard**: KPI metric cards, revenue trends, quick action toggles, low stock alerts, and recent orders.
2. **Advanced Analytics**: Sales by channel, customer growth trends, traffic sources, top product rankings, and real CSV exports.
3. **Product Catalog Manager**: Rich text editor, skin attributes checklist, video demonstration uploader, and stock manager.
4. **Brand Showcases**: Featured brand stores and brand masterclass heritage video manager.
5. **Categories CMS**: Hierarchy ordering, thumbnail management, and navigation menu toggles.
6. **Order Fulfillment Studio**: 6-stage delivery tracker, itemized invoice calculations, shipping label generation, and customer communication.
7. **Clientele & VIP Customer Studio**: Customer spending tiers, addresses, order history, and concierge messaging.
8. **Promotions & Coupons**: Rule-based discount codes, usage limits, and expiration tracking.
9. **Homepage & Banner CMS**: Visual section manager, layout template presets, and real-time storefront synchronization.
10. **Dermatological Journal CMS**: Article publishing workflow, tags, character counters, and reader preview mode.
11. **Review Moderation Studio**: Customer review approval, star rating analyticsWidget, video stream inspection, and atelier reply composer.
12. **Skin Quiz Builder**: 3-column Question Studio Builder with drag-and-drop reordering, question image uploads, and recommendation rule routing.
13. **Returns & Refunds Studio**: Return policy compliance manager, reason breakdown donut chart, and stage inspection timeline.
14. **System Settings**: 12 configuration tabs (general, shipping, tax rates, notifications, backup export/import, staff permissions, cache clearance).

---

## 🚀 3. Quick Start Guide (Local Development)

### Prerequisites:
- Python 3.12+
- Node.js 20+ and npm

### 1. Python FastAPI Backend:
```powershell
cd python-backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Launch FastAPI server
python run.py
```
- API Base URL: `http://127.0.0.1:8000/api`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Service Health Check: `http://127.0.0.1:8000/api/health`

### 2. Vue Storefront (Port 5173):
```powershell
cd frontend
npm install
npm run dev
```
- Storefront URL: `http://localhost:5173/`

### 3. Vue Admin Atelier (Port 5174):
```powershell
cd admin
npm install
npm run dev
```
- Admin Console URL: `http://localhost:5174/`

---

## 🔑 4. Demo Credentials for Evaluation

- **Customer Demo Account (Storefront)**:
  - **Email**: `sreynich.chan@example.com`
  - **Password**: `password123`
  - **Clientele Tier**: *Luméa Radiant Gold* (320 reward points)

- **Administrator Demo Account (Admin Atelier)**:
  - **Email**: `admin@lumea.com`
  - **Password**: `password123`
  - **Role**: `admin` / Super Administrator

---

## 🧪 5. Automated Verification & Test Suites

The Luméa codebase is backed by an automated test suite executed in CI/CD on every push:

```powershell
# 1. Run Complete Backend PyTest Suite (99 Tests)
python -m pytest python-backend/tests test_flow_regressions.py test_security_transactions.py

# 2. Run REST API Endpoint Verification (30 Tests)
python python-backend/test_api.py

# 3. Run Storefront Client Flow Tests (8 Tests)
node --test frontend/tests/flows.test.mjs test_recommendations.mjs

# 4. Run Responsive Split Build QA Check
node .browser-qa/check-split.mjs
```

---

## 📡 6. Core REST API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and uptime | Public |
| `GET` | `/api/categories` | Categories with dynamic product count | Public |
| `GET` | `/api/products` | Filterable catalog with search & sorting | Public |
| `GET` | `/api/products/{slug}` | Product details, ingredients & reviews | Public |
| `POST` | `/api/auth/register` | Customer account registration | Public |
| `POST` | `/api/auth/login` | Bcrypt login with JWT issuance (Email or Phone) | Public |
| `POST` | `/api/auth/logout` | Session invalidation via token version increment | Authenticated |
| `GET` | `/api/auth/me` | Customer profile and reward balance | Authenticated |
| `POST` | `/api/orders` | Checkout submission (`LUM-XXXXXX` generator) | Public / Guest / User |
| `GET` | `/api/orders/{orderNumber}` | Order status and fulfillment timeline | Public / Token |
| `POST` | `/api/payments/khqr/generate` | Dynamic Bakong KHQR EMVCo TLV payload | Public |
| `POST` | `/api/payments/khqr/simulate-approve` | Defense demo instant bank clearance | Public |
| `POST` | `/api/returns` | Return request submission | Customer |
| `GET` | `/api/returns/{request_number}` | 7-stage return status timeline | Customer / Admin |
| `POST` | `/api/upload` | Validated image uploader (.jpg, .png, .webp) | Authenticated |
| `POST` | `/api/upload/video` | Video review stream uploader (.mp4, .webm) | Authenticated |
| `GET` | `/api/admin/stats` | Executive KPI and revenue aggregation | Admin |
| `GET` | `/api/admin/orders` | Orders management with pagination | Admin |
| `GET` | `/api/admin/customers` | Registered clientele database | Admin |
| `GET` | `/api/admin/settings` | Store configuration and tax rates | Admin |
