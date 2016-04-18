"""
WSGI config for intiSoft project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.name == "posix":
    #Linux
    settings = "intiSoft.settings"
else:
    #Windows
    settings = "intiSoft.settings_prod"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()
