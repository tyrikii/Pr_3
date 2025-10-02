FROM python:3.13.7-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файлов требований
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Экспозиция порта
EXPOSE 8000

# Запуск приложения
CMD ["python", "app/app.py"]
