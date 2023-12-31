from pathlib import Path

import tomli
from starlette.config import Config

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent

config = Config(f"{str(BASE_PATH)}/.env")

with open(f"{BASE_PATH}/pyproject.toml", "rb") as reader:
    pyproject = tomli.load(reader)
    poetry = pyproject["tool"]["poetry"]
    information = pyproject["information"]

# API
PROJECT_DESCRIPTION_API = config("PROJECT_DESCRIPTION_API", cast=str, default=poetry.get("description"))
PROJECT_VERSION_API = config("PROJECT_VERSION_API", cast=str, default=poetry.get("version"))
PROJECT_NAME_API = config("PROJECT_NAME_API", cast=str, default=poetry.get("name"))
PROJECT_CONTACT_API = config(
    "PROJECT_AUTHORS_API",
    cast=dict,
    default={
        "name": information.get("contact")[0],
        "email": information.get("contact")[1],
    },
)
BASIC_HEADERS = {"Content-Type": "application/json", "accept": "application/json"}

# Postgres Database
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_HOST = config("DATABASE_HOST", cast=str, default="localhost")
DATABASE_NAME = config("DATABASE_NAME", cast=str, default="solfacil_local_dev")
DATABASE_USER = config("DATABASE_USER", cast=str, default="solfacil_local_dev")
DATABASE_PASS = config("DATABASE_PASS", cast=str, default="solfacil_local_dev")

# Testing
TESTING = config("TESTING", cast=bool, default=False)
TESTING_TEMPORAL_DATABASE = "postgres"

if TESTING:
    DATABASE_NAME += "_test"

# Postgres Database Url
DATABASE_URL = config(
    "DATABASE_URL",
    cast=str,
    default=f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
)

DATABASE_SCHEMA = config("DATABASE_SCHEMA", cast=str, default="public")

# MODE for environment
MODE = config("MODE", cast=str, default="DEV")

# Sentry SDK
SENTRY_SDK_DSN = config(
    "SENTRY_SDK_DSN",
    cast=str,
    default="https://8c4e3a8d64854c79afd488e1f8d9c9fa@o302946.ingest.sentry.io/4504407191650304",
)

# Gunicorn
GUNICORN_BIND = config("GUNICORN_BIND", cast=str, default="0.0.0.0:8000")
GUNICORN_WORKER_CLASS = config("GUNICORN_WORKER_CLASS", cast=str, default="uvicorn.workers.UvicornWorker")
GUNICORN_WORKERS_PER_CORE = config("GUNICORN_WORKERS_PER_CORE", cast=int, default=1)
GUNICORN_WORKERS = config("GUNICORN_WORKERS", cast=int, default=0)
GUNICORN_KEEPALIVE = config("GUNICORN_KEEPALIVE", cast=int, default=5)
GUNICORN_GRACEFUL_TIMEOUT = config("GUNICORN_GRACEFUL_TIMEOUT", cast=int, default=120)
GUNICORN_TIMEOUT = config("GUNICORN_TIMEOUT", cast=int, default=120)

# External services
MAX_ATTEMPTS = 5
REQUEST_TIMEOUT = 99
TIME_SLEEP = 1
VERIFY = True

# SSO - Keycloak
KEYCLOAK_BASE_URL = config("KEYCLOAK_BASE_URL", cast=str, default="")
KEYCLOAK_REALM = config("KEYCLOAK_REALM", cast=str, default="dev")

# Authentication
AUTH_CACHE_EXPIRATION = config("AUTH_CACHE_EXPIRATION", cast=int, default=2700)  # 45 minutes - 2700 seconds
AUTH_CACHE_MAXSIZE = config("AUTH_CACHE_MAXSIZE", cast=int, default=1024)  # items in cache

# Authentication with fixed token
ACCESS_VALIDATION = config("ACCESS_VALIDATION", cast=bool, default=False)
BEARER_TOKEN = config("BEARER_TOKEN", cast=str, default="")

# Temporal Envs
# for create new financing
DEFAULT_CALCULATOR = config("DEFAULT_CALCULATOR", cast=int, default=70)
DEFAULT_CITY = config("DEFAULT_CITY", cast=int, default=18)
DEFAULT_PROVIDER = config("DEFAULT_PROVIDER", cast=int, default=1)

# for create new Modelo de Recebimento
DEFAULT_EMAIL_PROVIDER = config("DEFAULT_EMAIL_PROVIDER", cast=str, default=False)
DEFAULT_STORE_PROVIDER = config("DEFAULT_STORE_PROVIDER", cast=int, default=False)
