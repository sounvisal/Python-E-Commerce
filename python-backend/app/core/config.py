import os
import secrets
import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

# Ensure local .env is loaded
load_dotenv()

logger = logging.getLogger("lumea.config")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Luméa E-Commerce API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security: Read from .env, generate secure cryptographic fallback if missing
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
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

if not settings.SECRET_KEY:
    # Generate cryptographically strong key if none provided in environment
    settings.SECRET_KEY = secrets.token_hex(32)
    logger.warning("No SECRET_KEY defined in environment/.env! Generated a secure 256-bit runtime key.")
