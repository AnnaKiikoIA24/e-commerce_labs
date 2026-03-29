from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.db import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
def health():
    """
    Health Check endpoint:
    - 200 OK, якщо база доступна
    - 503 Service Unavailable, якщо база недоступна
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("DB health check passed")
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except (SQLAlchemyError, OperationalError) as e:
        logger.error(f"DB health check failed: {e}")
        return JSONResponse(content={"status": "db down"}, status_code=503)