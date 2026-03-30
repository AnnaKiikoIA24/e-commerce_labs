# Базовий образ Python
FROM python:3.11-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Скопіювати файл залежностей і встановити пакети
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати весь код додатку
COPY . .

# Відкритий порт, якщо хочеш доступ до FastAPI (опційно)
EXPOSE 8000

# Запуск FastAPI через uvicorn
# Замінити 'main:app' на твій файл з FastAPI, якщо назва відрізняється
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]