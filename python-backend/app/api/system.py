from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
import logging
from datetime import datetime, timezone
import time
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db

router = APIRouter()
SERVER_START_TIME = time.time()

class NewsletterSubscribeRequest(BaseModel):
    email: EmailStr

@router.post("/newsletter")
def subscribe_newsletter(payload: NewsletterSubscribeRequest):
    """
    Register an email for Luméa botanical insights, promotions, and formulations newsletter.
    """
    clean_email = str(payload.email).strip().lower()
    return {
        "status": "success",
        "message": f"Successfully subscribed {clean_email} to Luméa editorial bulletins.",
        "email": clean_email,
        "subscribed_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/live", include_in_schema=False)
def liveness_check():
    return {"status": "alive"}


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive service health and database readiness check for production monitoring.
    """
    uptime_seconds = int(time.time() - SERVER_START_TIME)
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        logging.getLogger(__name__).warning("Database health check failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "degraded",
                "service": "Luméa E-Commerce API (Python FastAPI)",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": uptime_seconds,
                "database": "unavailable"
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
