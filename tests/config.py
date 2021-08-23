from foodgram.settings import *  # noqa, pylint: disable=unused-wildcard-import

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
SECRET_KEY = 'regular key for tests'
