# FastAPI Project with uv

Навчальний проєкт для ознайомлення з менеджером пакетів **uv**, фреймворком **FastAPI**, лінтером **Ruff** та системою автоматичних перевірок **pre-commit**.

## Вимоги

Перед початком роботи необхідно встановити:

* Python 3.10+
* uv
* Git

## Встановлення проєкту

Клонуйте репозиторій:

```bash
git clone <repository_url>
cd <project_name>
```

Синхронізуйте залежності:

```bash
uv sync
```

## Запуск проєкту

Запустіть FastAPI застосунок:

```bash
uv run fastapi dev main.py
```

Після запуску застосунок буде доступний за адресою:

```text
http://127.0.0.1:8000
```

Головний маршрут:

```text
GET /
```

Очікувана відповідь:

```json
{
  "message": "Hello World!"
}
```

## Перевірка якості коду

Запуск усіх pre-commit перевірок:

```bash
uv run pre-commit run --all-files
```

Запуск Ruff вручну:

```bash
uv run ruff check .
```

Форматування коду:

```bash
uv run ruff format .
```

## Структура проєкту

```text
.
├── main.py
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
└── .pre-commit-config.yaml
```

## Використані технології

* FastAPI
* uv
* Ruff
* pre-commit
* Git

## Автор

Когут Богдан Васильвич

Студентський навчальний проєкт.
