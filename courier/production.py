# settings/prod.py

from .base import *
from decouple import config


SECRET_KEY = os.environ.get("SECRET_KEY")

# Override common settings
DEBUG = True
# Add your production domain to ALLOWED_HOSTS
ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "https://cargofex.vercel.app",
    "https://cargofex.com",
    "https://www.cargofex.com",
    "https://www.cargofex.vercel.app",
]


# Set up the database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
    "SECURE": True,
}

# static files in src folder

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
