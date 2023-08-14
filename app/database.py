import os
import pickle
import sqlalchemy
from ddtrace import Pin, patch  # Datadog's tracing library for Python.
                                # It is used to trace requests as they flow across web servers,
                                # databases and microservices so that developers have great visibility into bottlenecks and troublesome requests.
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.declarative import declarative_base
from app.enum import BuildEnvironment

from app.internal.config import DATABASE_URL, TESTING
from app.internal.config.settings import MODE, PROJECT_NAME_API

if TESTING:
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)
    create_database(DATABASE_URL)

metadata_pickle_filename = "binary_db_metadata"
cache_path = os.path.join(os.getcwd(), ".sqlalchemy_cache")
cached_metadata = None


try:
    if MODE == BuildEnvironment.prd:
        patch(sqlalchemy=True)  # patch before importing `create_engine`

    engine = sqlalchemy.create_engine(DATABASE_URL, pool_pre_ping=True)
    logger.success("[+] Create database engine")

    if MODE == BuildEnvironment.prd:
        Pin.override(engine, service=PROJECT_NAME_API + "-sqlalchemy")  # Use a PIN to specify metadata engine

except SQLAlchemyError as error:
    logger.opt(exception=True).error(f"[-] Error connecting to {DATABASE_URL}: {error}")
    raise


try:
    with open(os.path.join(cache_path, metadata_pickle_filename), 'rb') as cache_file:
        cached_metadata = pickle.load(file=cache_file)
except IOError:
    # cache file not found - no problem, reflect as usual
    logger.warning("[-] Cache database metadata file not found")
    pass

if cached_metadata:
    Base = automap_base(declarative_base(bind=engine, metadata=cached_metadata))
    Base.prepare()
else:
    logger.warning("[-] Automap base it will take a while, be patient :)")
    Base = automap_base()
    Base.prepare(engine, reflect=True)  # reflect the tables

    # save the metadata for future runs
    try:
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        # make sure to open in binary mode - we're writing bytes, not str
        with open(os.path.join(cache_path, metadata_pickle_filename), 'wb') as cache_file:
            pickle.dump(Base.metadata, cache_file)
    except Exception as e:
        # couldn't write the file for some reason
        logger.error(f"[-] Error writing cache file: {e}")
        pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
