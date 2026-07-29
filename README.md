# Terrarium Manager

Django-приложение для учёта террариумных животных: кормление, здоровье, разведение, генетика, отчёты и API.

**Python:** 3.10–3.14 (рекомендуется 3.14) · **Django:** 6.x

## Быстрый старт

```bash
cp .env.example .env
py -3.14 -m pip install -r requirements.txt
py -3.14 manage.py migrate
py -3.14 manage.py seed_species
py -3.14 manage.py createsuperuser
py -3.14 manage.py runserver
```

## Основные модули

| URL | Описание |
|-----|----------|
| `/dashboard/` | Дашборд: кормления, затраты, визиты |
| `/animals/` | CRUD животных, timeline, рекомендации по уходу |
| `/feeding/` | Расписание и история кормлений |
| `/reminders/` | Напоминания |
| `/reports/` | Отчёты и экспорт CSV |
| `/incubation/` | Инкубация |
| `/genetics/calculator/` | Калькулятор морф |
| `/api/v1/` | REST API |
| `/api/docs/` | OpenAPI Swagger |

## Тесты

```bash
pytest
python manage.py check
```

## Docker

```bash
docker compose up --build
```

## Cron

```bash
python manage.py generate_reminders
```

## Переменные окружения

См. [`.env.example`](.env.example).

## Production checklist

- `DEBUG=False`
- Postgres (`DB_ENGINE=django.db.backends.postgresql`, `DB_PASSWORD=...`)
- `USE_REDIS=True`
- `EMAIL_BACKEND` / SMTP vars (по умолчанию SMTP при `DEBUG=False`)
- `CSRF_TRUSTED_ORIGINS` для вашего домена
- Раздача `MEDIA` через nginx/S3 (WhiteNoise отдаёт только static)
- `SENTRY_DSN` для мониторинга
- HTTPS + при необходимости `BEHIND_TLS_PROXY=True`
- `docker compose` / migrate перед стартом web
