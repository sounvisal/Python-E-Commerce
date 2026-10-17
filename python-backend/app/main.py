import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
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
    settings as settings_api
)
from app.seed.seed_data import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup: Create tables if not exist
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed database with initial catalog data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
        
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="RESTful API for the Luméa E-Commerce Platform built with Python FastAPI, SQLAlchemy, and SQLite.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Vue 3 client communication
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

# Serve static images and videos directly from backend for direct API inspection
static_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public", "images"))
if os.path.exists(static_images_dir):
    app.mount("/images", StaticFiles(directory=static_images_dir), name="images")

static_videos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public", "videos"))
os.makedirs(static_videos_dir, exist_ok=True)
app.mount("/videos", StaticFiles(directory=static_videos_dir), name="videos")

@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root to interactive Swagger UI documentation."""
    return RedirectResponse(url="/docs")
