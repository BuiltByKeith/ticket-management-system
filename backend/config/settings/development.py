# config/settings/development.py

from .base import *

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default port
]

CORS_ALLOW_CREDENTIALS = True