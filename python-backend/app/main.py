import os
import time
import logging
import asyncio
from contextlib import suppress
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.migrations import migrate_schema
from app.core.rate_limit import RateLimitMiddleware
from app.api import (
    system,
    categories,
    products,
    orders,
    auth,
    banners,
    pages,
    articles,
    returns,
    admin,
    upload,
    reviews,
    quizzes,
    settings as settings_api,
    payments
)
from app.seed.seed_data import seed_database
from app.api import promotions, contact
from app.services.order_lifecycle import expire_pending_orders

def sweep_expired_checkouts():
    db = SessionLocal()
    try:
        expire_pending_orders(db)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception('Could not expire pending checkouts')
    finally:
        db.close()

async def checkout_expiry_worker():
    while True:
        await asyncio.to_thread(sweep_expired_checkouts)
        await asyncio.sleep(30)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("lumea.server")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup: Create tables if not exist
    Base.metadata.create_all(bind=engine)
    migrate_schema(engine, seed_demo_promotions=not settings.PRODUCTION)
    
    # 2. Seed database with initial catalog data (idempotent; seeds if empty)
    with SessionLocal() as db:
        seed_database(db)
        
    logger.info("Luméa Atelier E-Commerce backend service initialized successfully.")
    expiry_worker = asyncio.create_task(checkout_expiry_worker())
    try:
        yield
    finally:
        expiry_worker.cancel()
        with suppress(asyncio.CancelledError):
            await expiry_worker
    logger.info("Luméa Atelier E-Commerce backend service shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="RESTful API for the Luméa E-Commerce Platform.",
    lifespan=lifespan,
    docs_url=None if settings.PRODUCTION else "/docs",
    redoc_url=None if settings.PRODUCTION else "/redoc",
    openapi_url=None if settings.PRODUCTION else "/openapi.json",
)

# 1. Security Headers & Request Timing Middleware
@app.middleware("http")
async def security_and_timing_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000

    # Timing header for observability
    response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"

    # OWASP Recommended Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Structured request logging
    if not request.url.path.startswith(("/images", "/videos")) and request.url.path != f"{settings.API_V1_STR}/live":
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)")

    return response

# 2. Rate Limiting Middleware (Brute-force & DDoS mitigation)
app.add_middleware(RateLimitMiddleware)

# 3. CORS configuration for Vue 3 storefront & admin SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api
app.include_router(system.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(products.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(banners.router, prefix=settings.API_V1_STR)
app.include_router(pages.router, prefix=settings.API_V1_STR)
app.include_router(articles.router, prefix=settings.API_V1_STR)
app.include_router(returns.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(upload.router, prefix=settings.API_V1_STR)
app.include_router(reviews.router, prefix=settings.API_V1_STR)
app.include_router(quizzes.router, prefix=settings.API_V1_STR)
app.include_router(settings_api.router, prefix=settings.API_V1_STR)
app.include_router(payments.router, prefix=settings.API_V1_STR)
app.include_router(promotions.router, prefix=settings.API_V1_STR)
app.include_router(contact.router, prefix=settings.API_V1_STR)

class VueFiles(StaticFiles):
    async def get_response(self, path, scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as error:
            first_segment = Path(path).parts[:1]
            if error.status_code != 404 or Path(path).suffix or first_segment in {
                ("api",), ("assets",), ("images",), ("videos",)
            }:
                raise
            return await super().get_response("index.html", scope)


project_root = Path(__file__).resolve().parents[2]
from app.api.upload import UPLOADS_DIR, VIDEOS_DIR, ensure_directories
ensure_directories()

# Dedicated mounts for uploaded media (survives restarts and aligns write/read paths)
app.mount("/images/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploaded_images")
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="uploaded_videos")

if settings.SERVE_BUILT_APPS:
    admin_build = project_root / "admin" / "dist"
    storefront_build = project_root / "frontend" / "dist"

    storefront_build.mkdir(parents=True, exist_ok=True)
    (storefront_build / "images").mkdir(parents=True, exist_ok=True)
    admin_build.mkdir(parents=True, exist_ok=True)
    (admin_build / "images").mkdir(parents=True, exist_ok=True)

    # Both apps use root-relative catalog paths. Prefer the storefront copy
    # on overlap while serving admin-specific images from its build.
    class SharedImages(StaticFiles):
        def __init__(self):
            super().__init__(directory=storefront_build / "images")
            self.all_directories.append(admin_build / "images")

    app.mount("/images", SharedImages(), name="images")
    app.mount("/atelier", VueFiles(directory=admin_build, html=True), name="admin")
    app.mount("/", VueFiles(directory=storefront_build, html=True), name="storefront")
else:
    static_images_dir = project_root / "frontend" / "public" / "images"
    if static_images_dir.exists():
        app.mount("/images", StaticFiles(directory=static_images_dir), name="images")

    @app.get("/", include_in_schema=False)
    def root_redirect():
        return RedirectResponse(url="/docs")
