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

## Фоновые задачи

```bash
celery -A terrarium_manager worker -l info
celery -A terrarium_manager beat -l info
```

Celery Beat каждый час генерирует напоминания и в 08:00 по часовому поясу
`Europe/Moscow` отправляет просроченные и сегодняшние напоминания.

## Telegram

Задайте `TELEGRAM_BOT_TOKEN`, настройте webhook бота на
`https://your-host/accounts/telegram/webhook/`, затем откройте
`/accounts/telegram/link/` и отправьте показанную команду боту.

## Резервное копирование

Скрипт использует `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` и
`DB_PASSWORD` (или `DB_PASS`) и сохраняет SQL в каталог `backups/`:

```bash
sh scripts/backup_db.sh
```

## Медиафайлы

Загруженные фотографии находятся в `MEDIA_ROOT` (`media/` по умолчанию).
В production раздавайте `/media/` через nginx или объектное хранилище и
резервируйте этот каталог отдельно от базы данных.

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
