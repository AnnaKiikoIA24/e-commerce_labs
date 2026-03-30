from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes import router
from app.logging import setup_logging
from app.migrations_util import run_migrations
import threading
import signal
import sys
import logging
from sqlalchemy.exc import OperationalError
from app.db import SessionLocal
from app.bot import start_bot

app = FastAPI()
app.include_router(router)

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Application initialized", extra={"event": "init"})

def shutdown(signal_num, frame):
    logger.info("SIGTERM received. Starting graceful shutdown...", extra={"event": "shutdown"})
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)

@app.get("/health")
@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except OperationalError:
        return JSONResponse(content={"status": "db down"}, status_code=503)

from app.bot import start_bot

@app.on_event("startup")
def startup_event():
    logger.info("Running migrations...", extra={"event": "startup"})
    run_migrations()

    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot thread started", extra={"event": "bot_start"})