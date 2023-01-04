FROM python:3.10

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

# where your code lives
WORKDIR $SERVICE_HOME

# Install poetry:
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

# copy whole project to your docker home directory.
COPY . ./

# run this command to install all dependencies
RUN poetry lock --no-update && \
    poetry install --only main

EXPOSE 8000

# Run gunicorn
CMD ["sh", "./startup.sh"]