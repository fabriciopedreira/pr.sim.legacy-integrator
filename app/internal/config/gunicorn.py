import multiprocessing

from app.internal.config import (
    GUNICORN_BIND,
    GUNICORN_GRACEFUL_TIMEOUT,
    GUNICORN_KEEPALIVE,
    GUNICORN_TIMEOUT,
    GUNICORN_WORKER_CLASS,
    GUNICORN_WORKERS,
    GUNICORN_WORKERS_PER_CORE,
    Logger,
)

# Host and port
bind = GUNICORN_BIND  # pylint: disable=invalid-name

# Workers
worker_class = GUNICORN_WORKER_CLASS  # pylint: disable=invalid-name
workers_per_core = GUNICORN_WORKERS_PER_CORE  # pylint: disable=invalid-name
cores = multiprocessing.cpu_count() // 2  # pylint: disable=invalid-name
default_web_concurrency = workers_per_core * cores  # pylint: disable=invalid-name
default_web_concurrency = max(int(default_web_concurrency), 2)  # pylint: disable=invalid-name
workers = GUNICORN_WORKERS or default_web_concurrency  # pylint: disable=invalid-name

# Logs
logger_class = Logger  # pylint: disable=invalid-name

# Timeouts
keepalive = GUNICORN_KEEPALIVE  # pylint: disable=invalid-name
graceful_timeout = GUNICORN_GRACEFUL_TIMEOUT  # pylint: disable=invalid-name
timeout = GUNICORN_TIMEOUT  # pylint: disable=invalid-name


# Debug Gunicorn configurations
LOG_DATA = {
    "bind": bind,
    "worker_class": worker_class,
    "workers_per_core": workers_per_core,
    "cores": cores,
    "workers": workers,
    "keepalive": keepalive,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "wsgi_app": "app.main:application",
}
