# settings/dev.py

from .base import *

# Override common settings
DEBUG = True
ALLOWED_HOSTS = [
    "*",
    "http://localhost:3000",
]
SECRET_KEY = "django-insecure-^@=5ey4e)klh8ov(qw8gdbrsyq7)%@0x)$@i)pittt^dnt#bta"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:9000",
    "http://172.20.10.4:3000",
    "http://172.20.10.3:3000",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
    "SECURE": False,
}
