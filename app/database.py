import sqlalchemy
from ddtrace import Pin, patch
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.internal.config import DATABASE_SCHEMA, DATABASE_URL, TESTING
from app.internal.config.settings import MODE, PROJECT_NAME_API

if TESTING:
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)

    create_database(DATABASE_URL)


# Postgres Database Configuration
try:
    if MODE == "PRD":
        patch(sqlalchemy=True)  # patch before importing `create_engine`

    engine = sqlalchemy.create_engine(DATABASE_URL, pool_pre_ping=True)

    if not engine.dialect.has_schema(engine, DATABASE_SCHEMA):
        engine.execute(CreateSchema(DATABASE_SCHEMA))

    logger.success("[+] Create database engine")

    if MODE == "PRD":
        Pin.override(engine, service=PROJECT_NAME_API + "-sqlalchemy")  # Use a PIN to specify metadata engine
except SQLAlchemyError as error:
    logger.opt(exception=True).error(f"[-] Error connecting to {DATABASE_URL}: {error}")
    raise


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
