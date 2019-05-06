#!/bin/sh
export UWSGI_PORT=9090
export DEBUG=0
exec uwsgi uwsgi.ini
