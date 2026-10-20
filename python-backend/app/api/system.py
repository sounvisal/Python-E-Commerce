from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import time
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()
SERVER_START_TIME = time.time()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive service health and database readiness check for production monitoring.
    """
    uptime_seconds = int(time.time() - SERVER_START_TIME)
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "degraded",
                "service": "Luméa E-Commerce API (Python FastAPI)",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": uptime_seconds,
                "database": db_status
            }
        )

    return {
        "status": "healthy",
        "service": "Luméa E-Commerce API (Python FastAPI)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime_seconds,
        "database": db_status,
        "version": "1.0.0"
    }
