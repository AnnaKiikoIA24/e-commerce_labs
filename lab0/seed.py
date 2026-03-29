from app.db import SessionLocal
from app.models import Schedule

db = SessionLocal()

lesson1 = Schedule(day="Monday", time="08:00", lesson="Math")
lesson2 = Schedule(day="Monday", time="09:00", lesson="English")

db.add_all([lesson1, lesson2])
db.commit()

print("Seed data added!")