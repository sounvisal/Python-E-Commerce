from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Luméa E-Commerce API (Python FastAPI)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "SQLite / SQLAlchemy ORM"
    }
