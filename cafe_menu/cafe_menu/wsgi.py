"""
WSGI config for cafe_menu project.
"""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafe_menu.settings")

application = get_wsgi_application()


