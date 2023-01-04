import pytest
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.database import engine, set_up_database_tables
from app.dependencies import get_session_db
from app.domain.patner_example.model import PatnerExample
from app.internal.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PORT, DATABASE_USER
from app.internal.config.settings import DATABASE_PASS, DATABASE_SCHEMA


@pytest.fixture
def postgres_uri():
    return f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:" f"{DATABASE_PORT}/{DATABASE_NAME}"


def test_engine(postgres_uri):
    assert str(engine.url) == postgres_uri
    assert "_test" in DATABASE_NAME


def test_set_up_database_tables():
    set_up_database_tables()

    with engine.connect() as conn:
        meta = MetaData(conn, schema=DATABASE_SCHEMA)
        meta.reflect(views=True)
        table_names = list(meta.tables.keys())

    assert f"{DATABASE_SCHEMA}.{PatnerExample.__tablename__}" in table_names


def test_get_session_db():
    generator = get_session_db()
    db = next(generator)

    assert isinstance(db, Session)
