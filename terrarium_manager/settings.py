import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

DB_HOST = env.str("DB_HOST")  # логин учётки биллинга
DB_LOGIN = env.str("DB_LOGIN")  # логин учётки биллинга
DB_PASS = env.str("DB_PASS")  # пароль учётки биллинга
DB_NAME = env.str("DB_NAME")  # адрес api
DB_PORT = env.str("DB_PORT")  # путь к драйверу api
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env.str('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']
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


    'accounts',
    'dashboard',
    'animals',
    'feeding',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = 'dashboard:dashboard'
LOGIN_URL = 'accounts:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Для разработки

AUTH_USER_MODEL = 'accounts.User'

LOGOUT_REDIRECT_URL = 'home'


EMAIL_HOST = 'smtp.yourserver.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'Terrarium Manager <noreply@yourdomain.com>'

ADMINS = [('Admin Name', 'admin@example.com')]

handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'


GRAPPELLI_ADMIN_TITLE = 'Terrarium Manager'
GRAPPELLI_INDEX_DASHBOARD = 'accounts.dashboard.CustomIndexDashboard'

SELECT2_CSS = 'css/select2/select2.min.css'
SELECT2_JS = 'js/select2/select2.full.js'
# SELECT2_JS = [f'{STATIC_ROOT}/script/select2.min.js']
# SELECT2_CSS = [f'{STATIC_ROOT}/style/select2.min.css']

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

USE_THOUSAND_SEPARATOR = True

