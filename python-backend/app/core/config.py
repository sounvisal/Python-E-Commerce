import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Luméa E-Commerce API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = "lumea-secret-key-for-jwt-tokens-academic-final-project-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: Absolute path to lumea.db in python-backend directory
    DATABASE_URL: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lumea.db').replace(chr(92), '/')}"
    
    # CORS: Allow Vue frontend
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
