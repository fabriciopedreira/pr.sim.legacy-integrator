from app.internal.config.gunicorn import (
    LOG_DATA,
    accesslog,
    bind,
    capture_output,
    cores,
    errorlog,
    keepalive,
    loglevel,
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
    assert isinstance(capture_output, bool)
    assert isinstance(accesslog, str)
    assert isinstance(errorlog, str)
    assert isinstance(loglevel, str)
    assert isinstance(keepalive, int)
