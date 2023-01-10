import pytest
from sqlalchemy.orm import Session

from app.database import engine
from app.dependencies import get_session_db
from app.internal.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PORT, DATABASE_USER
from app.internal.config.settings import DATABASE_PASS


@pytest.fixture
def postgres_uri():
    return f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:" f"{DATABASE_PORT}/{DATABASE_NAME}"


def test_engine(postgres_uri):
    assert str(engine.url) == postgres_uri
    assert "_test" in DATABASE_NAME


def test_get_session_db():
    generator = get_session_db()
    db = next(generator)

    assert isinstance(db, Session)
