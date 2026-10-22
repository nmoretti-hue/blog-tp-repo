"""PythonAnywhere configuration. Secrets stay outside the repository."""
import os
from pathlib import Path
from .settings import *  # noqa: F401,F403

DEBUG = False
SECRET_KEY = Path.home().joinpath('.blog-secret-key').read_text().strip()
ALLOWED_HOSTS = ['nicomore999.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://nicomore999.pythonanywhere.com']
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [item for item in MIDDLEWARE if not item.startswith('debug_toolbar.')]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
DATABASES['default']['NAME'] = Path.home() / 'blog-data' / 'db.sqlite3'
MEDIA_ROOT = Path.home() / 'blog-data' / 'media'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
