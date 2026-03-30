import threading
import logging
import structlog
from contextlib import suppress
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes import router
from app.logging import setup_logging
from app.migrations_util import run_migrations
from sqlalchemy.exc import OperationalError
from app.db import SessionLocal
from app.bot import start_bot

logging.basicConfig(format="%(message)s", level=logging.INFO)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()

app = FastAPI()
app.include_router(router)

setup_logging()
logger.info("Application initialized", extra={"event": "init"})

def run_migrations_safe():
    try:
        run_migrations()
        logger.info("Migrations ran successfully", extra={"event": "migrations"})
    except OperationalError as e:
        logger.warning(f"Database unavailable, skipping migrations: {e}", extra={"event": "migrations_skip"})
    except Exception as e:
        logger.error(f"Migration failed, skipping: {e}", extra={"event": "migrations_skip"})

@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except OperationalError:
        return JSONResponse(content={"status": "db down"}, status_code=503)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations_safe()

    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started", extra={"event": "bot_start"})

    yield

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)