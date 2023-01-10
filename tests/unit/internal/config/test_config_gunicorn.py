from app.internal.config import Logger
from app.internal.config.gunicorn import (
    LOG_DATA,
    bind,
    cores,
    keepalive,
    logger_class,
    worker_class,
    workers,
    workers_per_core,
)


def test_configs_gunicorn():
    assert worker_class == "uvicorn.workers.UvicornWorker"
    assert LOG_DATA["wsgi_app"] == "app.main:application"
    assert workers_per_core > 0

    assert isinstance(bind, str)
    assert isinstance(cores, int)
    assert isinstance(workers, int)
    assert isinstance(keepalive, int)
    assert logger_class == Logger
