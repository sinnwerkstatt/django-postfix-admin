from .base import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME')

INTERNAL_IPS = ('127.0.0.1',)

try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ModuleNotFoundError:
    pass

try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

except ModuleNotFoundError:
    pass

