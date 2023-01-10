import pytest
from loguru import logger
from sqlalchemy_utils.functions import drop_database

from app.database import Base, engine
from app.dependencies import get_session_db
from app.internal.config import DATABASE_URL


@pytest.fixture(scope="session")
def create_tables_db():
    if "_test" in DATABASE_URL:
        Base.metadata.create_all(bind=engine, checkfirst=True)


@pytest.fixture(scope="session")
def drop_db(request):
    @request.addfinalizer
    def drop_databases():
        if "_test" in DATABASE_URL:
            drop_database(DATABASE_URL)


@pytest.fixture
def session_db():
    return next(get_session_db())


@pytest.fixture
def cap_logger(caplog):
    handler_id = logger.add(caplog.handler, format="{message}")

    yield caplog

    logger.remove(handler_id)
