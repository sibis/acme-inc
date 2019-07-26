import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '=9n8m=xxg&bf=(u(7r*4&s3gz0-!bi&+zu3(q((qsd+%(r=_yb'

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'authentication_app.User'

AUTHENTICATION_BACKENDS = ['authentication_app.backends.EmailAuthBackend', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'djcelery',
    'channels',

    # Apps from django rest framework
    'rest_framework',
    'rest_framework.authtoken',

    # Custom apps
    'authentication_app',
    'acme_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acme_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'acme_project.wsgi.application'

ASGI_APPLICATION = 'acme_project.routing.application'

REDIS_URL = "redis://h:pad3793317702a41ee5b912f87f727ace4935306f10cc1e384b1514ffadeb3c41@ec2-3-220-50-71.compute-1" \
            ".amazonaws.com:10879 "

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

REST_FRAMEWORK = {
    # uncomment for production to disallow browsable APIs
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'acme',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Celery Configuration

CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = REDIS_URL

CELERY_AMQP_TASK_RESULT_EXPIRES = 6000

CELERY_TASK_RESULT_EXPIRES = None

CELERY_TIMEZONE = TIME_ZONE

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

ATTACHMENTS_DIR_NAME = 'attachments'

ATTACHMENT_MAX_FILE_UPLOAD_SIZE = 200 * 1024 * 1024  # 200 MB

DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024

ATTACHMENT_SUPPORTED_FILE_FORMATS = {
    'application/vnd.ms-excel': {'allow': True},
    'text/x-csv': {'allow': True},
    'text/plain': {'allow': True}
}
