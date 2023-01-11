############################
#  Making Base Image       #
############################
FROM python:3.10 as base

# setup environment variable
ENV SERVICE_HOME=/usr/src/application \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    MODE=DEV 

RUN apt-get update -y &&  \
    apt-get upgrade -y &&  \
    apt-get -y install netcat && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir $SERVICE_HOME

# copy whole project to your docker home directory.
COPY . ./
# Install poetry:
RUN pip3 install poetry && \
    poetry config virtualenvs.create false
# run this command to install all dependencies
RUN poetry lock --no-update && \
    poetry install --only main && \
    poetry add isort
   
EXPOSE 8000
# where your code lives
WORKDIR $SERVICE_HOME

############################
#  Static Code Check       #
############################
FROM base as tests
COPY . ./

RUN poetry run flake8 ./app ./tests && \
    poetry run pylint ./app/ && \
    poetry run mypy --ignore-missing-imports ./app/ && \
    poetry run bandit -v -r ./app/ "pyproject.toml"


############################
#  Unit Code Testing       #
############################
RUN pytest --cov

############################
#  Deploy Final Image      #
############################
FROM base as final
COPY . ./
# Run gunicorn
CMD ["sh", "./startup.sh"]
