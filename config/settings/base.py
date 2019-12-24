import environ

BASE_DIR = environ.Path(__file__) - 3  # type: environ.Path
# APPS_DIR = BASE_DIR.path('apps')

env = environ.Env()
env.read_env(BASE_DIR('.env'))

TIME_ZONE = 'Europe/Berlin'
SITE_ID = 1
LANGUAGE_CODE = 'de-de'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEBUG = env.bool('DJANGO_DEBUG', default=False)
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

DATABASES = {'default': env.db("DATABASE_URL")}
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default='localhost')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

ADMINS = (("BOFH", 'webmaster@localhost'),)
MANAGERS = ADMINS

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('static-collected')
# STATICFILES_DIRS = (
#     BASE_DIR('static'),
# )
MEDIA_ROOT = BASE_DIR('media')
MEDIA_URL = '/media/'
# LOCALE_PATHS = [BASE_DIR('config/locale')]
