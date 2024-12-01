# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Создаем директорию для конфигурационных файлов
RUN mkdir -p /app/config

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Windows PowerShell команда для запуска:
# docker run -p 8000:8000 -v ${PWD}/src/.env:/app/src/.env -v ${PWD}/src/api_keys.json:/app/src/api_keys.json python-executor