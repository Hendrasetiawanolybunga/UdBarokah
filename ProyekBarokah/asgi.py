# ProyekBarokah/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 1. Tambahkan panggilan django.setup() di sini
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyekBarokah.settings')
django.setup() 
# **********************************************

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import admin_dashboard.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": SessionMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter(
                admin_dashboard.routing.websocket_urlpatterns
            )
        )
    ),
})