import random
import string
from environ.environ import ImproperlyConfigured

from .base import *  # noqa

try:
    SECRET_KEY = env("DJANGO_SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = ''.join(
        [random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, '+-:$;<=>?@^_~')) for i in
         range(63)])
    with open('.env', 'a') as envfile:
        envfile.write('DJANGO_SECRET_KEY={}\n'.format(SECRET_KEY))
