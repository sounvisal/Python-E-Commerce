# Python-E-Commerce — LUMÉA Atelier System

> A full-stack contemporary e-commerce application featuring a **Python FastAPI REST API** backend, a **Vue 3 + Vite** storefront (Port 5173), and a dedicated **Vue 3 + Vite** Admin Atelier Dashboard (Port 5174).

---

## 🏗️ Architecture Overview

```
Python-E-Commerce/
├── python-backend/            # Python 3.12 + FastAPI REST API (Port 8000)
│   ├── app/
│   │   ├── api/               # REST Controllers (system, auth, categories, products, orders, banners, upload, reviews, quizzes, settings)
│   │   ├── core/              # Config, database session, JWT security
│   │   ├── models/            # SQLAlchemy 2.0 ORM models
│   │   ├── schemas/           # Pydantic v2 DTOs with validation
│   │   └── seed/              # Catalog fixture data and seeder
│   ├── lumea.db               # SQLite database (zero-config, portable)
│   ├── run.py                 # Uvicorn server launcher
│   └── test_api.py            # Automated test suite (26/26 passing, 100% success)
│
├── frontend/                  # Vue 3 Storefront SPA + Vite (Port 5173)
│   ├── src/
│   │   ├── components/        # Navbar, Footer, ProductCard, CartDrawer, etc.
│   │   ├── views/             # 40 Storefront views (Shop, Quiz, Routine, Account, etc.)
│   │   ├── stores/            # Pinia stores (cart, products, auth, wishlist)
│   │   ├── router/            # Vue Router with scroll restoration
│   │   └── assets/main.css    # Warm bisque aesthetic design tokens (#F5EFEB, #7A2E22)
│   └── vite.config.js         # Port 5173 with proxy /api -> http://127.0.0.1:8000
│
├── admin/                     # Vue 3 Admin Dashboard SPA + Vite (Port 5174)
│   ├── src/
│   │   ├── components/        # MetricCard, RevenueChart, CategoryDonutChart, ModalDialog, StatusBadge
│   │   ├── views/             # DashboardView, ProductsView, OrdersView, CategoriesView, CustomersView, SettingsView, LoginView
│   │   ├── stores/            # Pinia stores (auth, admin data & alerts)
│   │   ├── router/            # Vue Router with authenticated guards
│   │   └── assets/admin.css   # Dark executive atelier design tokens
│   └── vite.config.js         # Port 5174 with proxy /api -> http://127.0.0.1:8000
│
├── format/                    # High-resolution design mockups & UI specifications
├── AGENTS.md                  # Context & instructions for AI pair-programming agents
├── GEMINI.md                  # Complete system context and memory documentation
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup & Run (Python FastAPI)

```powershell
cd python-backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the FastAPI server
python run.py
```
- API Base URL: `http://127.0.0.1:8000/api`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Service Health Check: `http://127.0.0.1:8000/api/health`
- Run Automated Test Suite: `python test_api.py` (12/12 tests passing)

### 2. Frontend Storefront Setup & Run (Vue 3)

```powershell
cd frontend

npm install
npm run dev
```
- Storefront URL: `http://localhost:5173/`

### 3. Admin Dashboard Setup & Run (Vue 3)

```powershell
cd admin

npm install
npm run dev
```
- Admin Dashboard URL: `http://localhost:5174/`

---

## 🔑 Demo Credentials

- **Customer Demo (Storefront)**:
  - Email: `sreynich.chan@example.com`
  - Password: `password123`
  - Tier: *Luméa Radiant Gold* (320 pts)
- **Admin Atelier (Dashboard)**:
  - Email: `admin@lumea.com`
  - Password: `admin123`
  - *(Or use the 1-Click Demo Login on the login screen)*

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and timestamp |
| `GET` | `/api/categories` | 8 skincare categories with dynamic product counts |
| `GET` | `/api/products` | Catalog with search, filter (category, skin type, concern), and sort |
| `GET` | `/api/products/featured` | Signature & featured showcase items |
| `GET` | `/api/products/{slug}` | Product details with gallery, ingredients, and related items |
| `POST` | `/api/orders` | Place customer order with discount code & order generator (`LUM-XXXXXX`) |
| `GET` | `/api/orders/{orderNumber}` | Order details and tracking timeline |
| `POST` | `/api/auth/register` | Customer registration |
| `POST` | `/api/auth/login` | Bcrypt authenticated login with JWT token issuance |
| `GET` | `/api/auth/me` | Protected customer profile (`Authorization: Bearer <token>`) |
| `GET` | `/api/banners` | Page banner CMS items |
| `GET` | `/api/banners/{page}` | Banner configuration for specific page (`home`, `shop`, `deals`, etc.) |
