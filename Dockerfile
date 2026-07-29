FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build-time only — must NOT persist as ENV into the runtime image.
ARG SECRET_KEY=build-only-not-for-production
RUN SECRET_KEY=${SECRET_KEY} DEBUG=False ALLOWED_HOSTS=localhost \
    python manage.py collectstatic --noinput

CMD ["gunicorn", "terrarium_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
