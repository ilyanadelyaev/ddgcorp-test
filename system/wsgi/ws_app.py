import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings.prod')

import gevent.socket
import redis.connection

redis.connection.socket = gevent.socket

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()
