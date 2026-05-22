# SBR Test Task

Тестовое задание по автоматизации тестирования: UI (Playwright) + API (requests) + CI/CD (GitHub Actions)

## Allure отчёт

Актуальный отчёт о прогоне тестов доступен по ссылке: https://dmitrievich-an.github.io/sbr_test_task/

---

## Запуск локально

### Требования

- Python 3.11+
- Git

### 1. Клонировать репозиторий

```bash
git clone https://github.com/dmitrievich-an/sbr_test_task.git
cd sbr_test_task
```

### 2. Создать и активировать виртуальное окружение

```bash
# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Установить браузер Playwright

```bash
playwright install chromium
```

### 5. Создать файл .env

Создать файл `.env` в корне проекта со следующим содержимым:

```env
API_BASE_URL=https://restful-booker.herokuapp.com
UI_BASE_URL=https://practice.expandtesting.com
UI_LOGIN=practice
UI_PASSWORD=SuperSecretPassword!
API_USERNAME=admin
API_PASSWORD=password123
```

### 6. Запустить тесты

```bash
# Все тесты
pytest

# Только API тесты
pytest tests/api/

# Только UI тесты
pytest tests/ui/
```

### 7. Посмотреть Allure отчёт

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Запуск через Docker

### Требования

- Docker Desktop

### 1. Клонировать репозиторий

```bash
git clone https://github.com/dmitrievich-an/sbr_test_task.git
cd sbr_test_task
```

### 2. Создать файл .env

Создай файл `.env` в корне проекта (содержимое см. выше).

### 3. Запустить тесты

```bash
docker-compose up --build
```

### 4. Посмотреть Allure отчёт

```bash
allure serve allure-results
```

---

## Стек технологий

- **Python 3.13**
- **pytest** — фреймворк для тестирования
- **Playwright** — UI тесты
- **requests** — API тесты
- **Faker** — генерация тестовых данных
- **Allure** — отчётность
- **Docker** — контейнеризация
- **GitHub Actions** — CI/CD

---

## Структура проекта

```
sbr_test_task/
├── .github/workflows/    # GitHub Actions
├── helpers/              # Генераторы тестовых данных
├── pages/                # Page Object Model
├── tests/
│   ├── api/              # API тесты
│   └── ui/               # UI тесты
├── conftest.py           # Фикстуры
├── constants.py          # Константы
├── Dockerfile
├── docker-compose.yml
└── pytest.ini
```