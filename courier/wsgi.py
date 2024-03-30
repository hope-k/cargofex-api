"""
WSGI config for courier project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    (
        "courier.production"
        if config("PRODUCTION") == "True"
        else "courier.development"
    ),
)
application = get_wsgi_application()
app = application
