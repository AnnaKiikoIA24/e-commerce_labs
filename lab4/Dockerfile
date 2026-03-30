# Базовий образ Python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Відкритий порт тільки для API
EXPOSE 8000

# Запуск FastAPI + Bot
CMD ["python", "-u", "main.py"]