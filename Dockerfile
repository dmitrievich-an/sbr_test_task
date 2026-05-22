FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей для Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install -r requirements.txt

# Устанавливаем Playwright браузер со всеми системными зависимостями
RUN playwright install chromium
RUN playwright install-deps chromium

# Копируем весь проект
COPY . .

# Запускаем тесты
CMD ["pytest", "--alluredir=allure-results"]