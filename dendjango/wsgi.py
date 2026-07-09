"""
WSGI config for dendjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import sys
from pathlib import Path

# Add the parent directories to the Python path
path_root = Path(__file__).resolve().parent.parent
sys.path.append(str(path_root))

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dendjango.settings')

application = get_wsgi_application()
app = application