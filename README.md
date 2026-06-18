# Messages API

REST API для обміну повідомленнями між користувачами.

Додаток розроблений на базі FastAPI та PostgreSQL. Підтримує:

* створення повідомлень;
* редагування повідомлень;
* видалення повідомлень;
* завантаження файлів до повідомлень;
* отримання списку повідомлень;
* формування звітів по повідомленнях.

## Технології

* FastAPI
* SQLAlchemy Async
* PostgreSQL
* Alembic
* Docker
* Docker Compose
* uv

## Запуск проєкту

### 1. Клонувати репозиторій

```bash
git clone <repository_url>
cd <project_name>
```

### 2. Створити файл `.env`

Приклад:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_db

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/fastapi_db
```

### 3. Запустити контейнери

```bash
docker compose up --build
```

## Міграції бази даних

Після запуску контейнерів необхідно застосувати міграції Alembic.

Виконати команду:

```bash
docker compose exec web uv run alembic upgrade head
```

Якщо потрібно створити нову міграцію:

```bash
docker compose exec web uv run alembic revision --autogenerate -m "migration_name"
```

Після створення застосувати її:

```bash
docker compose exec web uv run alembic upgrade head
```

## Docker Compose

Проєкт складається з двох сервісів:

### web

FastAPI додаток.

* порт: 8000
* автоматичне перезавантаження при зміні коду

### db

PostgreSQL 15.

* порт: 5432
* збереження даних через Docker Volume

## Зупинка проєкту

```bash
docker compose down
```

Для видалення контейнерів разом із томами:

```bash
docker compose down -v
```
