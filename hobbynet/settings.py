import json
from pathlib import Path
import socket
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-wiesg1k1cf4)q==0oxrd1xk+)6&ct_b*(y)55tkvqx=@%3)7ob'

# Keep API keys in keys.json and keep keys.json in .gitignore
# This is for safety

keys_file = BASE_DIR / 'keys.json'
if keys_file.exists():
    with open('keys.json', 'r') as keys:
        KEYS = json.load(keys)
else:
    KEYS = {}

DEBUG = True
DEBUG_SERVER = socket.gethostname() == 'sernex'

ALLOWED_HOSTS = ['hobbynet.redttg.com', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'hobbynet.app_auth',
    'hobbynet.common',
    'hobbynet.profiles',
    'hobbynet.topics',
    'hobbynet.posts',

    'django_backblaze_b2',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
]

if DEBUG:
    del MIDDLEWARE[0]
    del MIDDLEWARE[-1]


ROOT_URLCONF = 'hobbynet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'hobbynet.wsgi.application'

# Postgres database setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hobbynet_development',
        'USER': 'redttg_postgres',
        'PASSWORD': 'django_softuni',
        'HOST': 'sernex',
        'PORT': '5432'
    }
}

# Password validators to check the passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

if not DEBUG_SERVER:
    AUTH_PASSWORD_VALIDATORS.clear()

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = KEYS.get('EMAIL_KEY', '')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'hobbynet@redttg.com'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app_auth.AccountModel'

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('profile_details_self')

PRIVACY_MODEL_CHOICES = [
    ('private', 'Private'),
    ('friends', 'Friends'),
    ('public', 'Public')
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://sernex:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": KEYS.get('REDIS_PASSWORD', '')
        },
        "KEY_PREFIX": "hobbynet_default"
    },
    "django-backblaze-b2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://sernex:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": KEYS.get('REDIS_PASSWORD', '')
        },
        "KEY_PREFIX": "django-backblaze-b2"
    },
}

if DEBUG:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }

BACKBLAZE_CONFIG = {
    # however you want to securely retrieve these values
    "application_key_id": KEYS.get('BACKBLAZE_KEY_ID', ''),
    "application_key": KEYS.get('BACKBLAZE_KEY', ''),
    "bucket": "HobbyNetMedia"
}

DEFAULT_FILE_STORAGE = 'django_backblaze_b2.storage.BackblazeB2Storage'

CSRF_TRUSTED_ORIGINS = [
    'https://hobbynet.redttg.com'
]

