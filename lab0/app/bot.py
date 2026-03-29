from aiogram import Bot, Dispatcher, types
from app.config import settings
from app.db import SessionLocal
from app.models import Schedule

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привіт! Напиши /schedule")

@dp.message_handler(commands=["schedule"])
async def get_schedule(msg: types.Message):
    try:
        db = SessionLocal()
        lessons = db.query(Schedule).all()
        text = "\n".join([f"{l.day} {l.time} - {l.lesson}" for l in lessons])
        await msg.answer(text or "Немає розкладу")
    except Exception:
        await msg.answer("База даних недоступна 😢")
    finally:
        if 'db' in locals():
            db.close()

def run_bot():
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())  # Створюємо новий event loop для потоку
    from aiogram import executor
    executor.start_polling(dp)

import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())