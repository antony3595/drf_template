import multiprocessing
from datetime import datetime

bind = ':9000'
max_requests = 1000
workers = multiprocessing.cpu_count() * 2 + 1

chdir = "/code"

loglevel = 'info'
accesslog = '/code/logs/gunicorn-access.log'
errorlog = '/code/logs/gunicorn-error.log'
env = "DJANGO_SETTINGS_MODULE=main.settings"
