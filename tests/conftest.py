import pytest
from loguru import logger
from sqlalchemy_utils.functions import drop_database

from app import set_up_database_tables
from app.internal.config import DATABASE_URL


@pytest.fixture(scope="session")
def drop_db(request):
    @request.addfinalizer
    def drop_databases():
        drop_database(DATABASE_URL)


@pytest.fixture(scope="session")
def create_tables_db():
    set_up_database_tables()


@pytest.fixture
def cap_logger(caplog):
    handler_id = logger.add(caplog.handler, format="{message}")

    yield caplog

    logger.remove(handler_id)
