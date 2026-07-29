import os
from pathlib import Path
from celery.schedules import crontab
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
SITE_URL = env.str('SITE_URL', default='http://localhost:8000')
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


INSTALLED_APPS = [
    'grappelli',
    'django_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_tables2',
    'django_filters',
    'imagekit',
    'rest_framework',
    'drf_spectacular',

    'accounts',
    'dashboard',
    'animals',
    'feeding',
    'health',
    'reminders',
    'incubation',
    'genetics',
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.ActivityLogMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]


if DEBUG:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

ROOT_URLCONF = 'terrarium_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'terrarium_manager.wsgi.application'

_db_engine = env.str('DB_ENGINE', default='django.db.backends.sqlite3')
if _db_engine == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': _db_engine,
            'NAME': env.str('DB_NAME'),
            'USER': env.str('DB_USER', default=''),
            'PASSWORD': env.str('DB_PASSWORD', default=env.str('DB_PASS', default='')),
            'HOST': env.str('DB_HOST', default=''),
            'PORT': env.str('DB_PORT', default=''),
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Terrarium Manager API',
    'VERSION': '1.0.0',
}

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/1')
CELERY_RESULT_BACKEND = env.str('CELERY_BROKER_URL', default='redis://127.0.0.1:6379/1')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULE = {
    'generate-reminders-hourly': {
        'task': 'reminders.tasks.generate_all_reminders',
        'schedule': crontab(minute=0),
    },
    'send-reminders-every-morning': {
        'task': 'reminders.tasks.send_reminder_emails',
        'schedule': crontab(hour=8, minute=0),
    },
}
TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN', default='')

SENTRY_DSN = env.str('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
    if env.bool('BEHIND_TLS_PROXY', default=False):
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if not DEBUG:
    STORAGES = {
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
else:
    STORAGES = {
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Каталоги справочника видов:
#  - popular: импортируем в БД сразу
#  - catalog: пользователь добавляет по мере необходимости
SPECIES_LIBRARY_POPULAR_PATH = BASE_DIR / 'data' / 'species_popular_ru.json'
SPECIES_LIBRARY_CATALOG_PATH = BASE_DIR / 'data' / 'species_catalog_ru.json'

# Legacy fallback (если новые файлы отсутствуют).
SPECIES_LIBRARY_PATH = BASE_DIR / 'data' / 'species_library_ru.json'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGIN_URL = 'accounts:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = env.str(
    'EMAIL_BACKEND',
    default=(
        'django.core.mail.backends.console.EmailBackend'
        if DEBUG
        else 'django.core.mail.backends.smtp.EmailBackend'
    ),
)

AUTH_USER_MODEL = 'accounts.User'

LOGOUT_REDIRECT_URL = 'accounts:login'

EMAIL_HOST = env.str('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default='Terrarium Manager <noreply@localhost>')

ADMINS = [('Admin Name', 'admin@example.com')]

handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'


GRAPPELLI_ADMIN_TITLE = 'Terrarium Manager'
GRAPPELLI_INDEX_DASHBOARD = 'accounts.dashboard.CustomIndexDashboard'

SELECT2_CSS = 'css/select2/select2.min.css'
SELECT2_JS = 'js/select2/select2.full.js'
# SELECT2_JS = [f'{STATIC_ROOT}/script/select2.min.js']
# SELECT2_CSS = [f'{STATIC_ROOT}/style/select2.min.css']

USE_REDIS = env.bool('USE_REDIS', default=False)

if USE_REDIS:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": env.str('REDIS_URL', default='redis://127.0.0.1:6379'),
        },
        "select2": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.str('REDIS_SELECT2_URL', default='redis://127.0.0.1:6379/2'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
        "select2": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    }

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=['http://localhost:8000', 'http://127.0.0.1:8000'],
)

USE_THOUSAND_SEPARATOR = True

