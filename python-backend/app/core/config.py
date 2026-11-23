import os
import secrets
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List, Literal

# Ensure local .env is loaded
load_dotenv()

logger = logging.getLogger("lumea.config")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Luméa E-Commerce API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security: Read from .env, generate secure cryptographic fallback if missing
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    PRODUCTION: bool = False
    SERVE_BUILT_APPS: bool = False
    ENABLE_DEMO_PAYMENTS: bool = False
    PAYWAY_ENVIRONMENT: Literal["sandbox", "live"] = "sandbox"
    PAYWAY_MERCHANT_ID: str = ""
    PAYWAY_API_KEY: str = ""
    PAYWAY_PUBLIC_URL: str = ""
    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: Absolute path to lumea.db in python-backend directory
    DATABASE_URL: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lumea.db').replace(chr(92), '/')}"
    
    # CORS: Explicitly allowed origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

def safe_db_url_str(url: str) -> str:
    try:
        from sqlalchemy.engine import make_url
        return make_url(url).render_as_string(hide_password=True)
    except Exception:
        return "[redacted-database-url]"

_runtime_generated_key = False
if not settings.SECRET_KEY:
    settings.SECRET_KEY = secrets.token_hex(32)
    _runtime_generated_key = True
    logger.warning("No SECRET_KEY defined in environment/.env! Generated a secure 256-bit runtime key.")

def validate_production_security(s: Settings):
    if not s.PRODUCTION:
        return
    if s.ENABLE_DEMO_PAYMENTS:
        s.ENABLE_DEMO_PAYMENTS = False
        logger.warning("Demo payments cannot be enabled in production. Overriding ENABLE_DEMO_PAYMENTS=False.")
    key = (s.SECRET_KEY or "").strip()
    if not key or len(key.encode("utf-8")) < 32 or (s is settings and _runtime_generated_key):
        raise ValueError("A stable SECRET_KEY of at least 32 bytes must be configured in environment/.env when PRODUCTION=True to prevent session invalidation.")
    if not s.DATABASE_URL.startswith(("postgresql://", "postgres://", "postgresql+psycopg://")):
        raise ValueError(
            f"PostgreSQL DATABASE_URL is required when PRODUCTION=True to prevent ephemeral data loss (found: {safe_db_url_str(s.DATABASE_URL)})."
        )

if settings.PRODUCTION:
    validate_production_security(settings)
