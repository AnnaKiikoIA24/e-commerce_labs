import threading
import logging
import structlog
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from fastapi import FastAPI, Response, status
import uvicorn
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.db import SessionLocal, engine
from app.models import Schedule, Base

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)
logger = structlog.get_logger()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    logger.info("bot_command", command="/start", user=msg.from_user.id)
    await msg.answer("Привіт! Напиши /schedule")


@dp.message_handler(commands=["schedule"])
async def get_schedule(msg: types.Message):
    db = SessionLocal()
    try:
        lessons = db.query(Schedule).all()
        text_msg = "\n".join([f"{l.day} {l.time} - {l.lesson}" for l in lessons])
        await msg.answer(text_msg or "Немає розкладу")
        logger.info("bot_command", command="/schedule", user=msg.from_user.id, result="ok")
    except Exception as e:
        await msg.answer("База даних недоступна 😢")
        logger.error("bot_command", command="/schedule", user=msg.from_user.id, error=str(e))
    finally:
        db.close()

app = FastAPI()


@app.get("/health")
def health(response: Response):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("health_check", status="ok")
        return {"status": "ok"}
    except SQLAlchemyError:
        logger.error("health_check", status="error", detail="Database not reachable")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "detail": "Database not reachable"}

def start_bot():
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    executor.start_polling(dp, loop=loop)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8080)