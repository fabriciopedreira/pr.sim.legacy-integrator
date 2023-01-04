
# API documentation - **Legacy Integrator (Simulation)**

This document presents the basic information of the **API - Legacy Integrator (Simulation)**. For more information, contact the developers at [Contacts](#4.Contacts).

# Version control

| Date       | Version | Description          | Author                    |
|------------|---------|----------------------|---------------------------|
| 04/03/2023 | 0.1.0   | Project creation     | **Frank Ricardo Ramirez** |

# Summary

1. [Product Overview](#1.-Product-Overview)

2. [Endpoint List](#2-Endpoint-List)

3. [Environment Preparation](#3.-Environment-Preparation)

4. [Contacts](#4.-Contacts)

# 1. Product Overview

|                              |                                                                  |
| -----------------------------|------------------------------------------------------------------|
| **The problem**              | Need to integrate with the company's legacy database.            |
| **Whose impact is**          | Getting out of legacy solutions such as Core and Legacy-project. |
| **A good solution would be** | Access the legacy database from a separate service.              |

# 2 Endpoint List

    URL: http://TODO.solfacil.com.br/
    Available environments: Stg e Prod

| EndPoint      | Occupation   |
|---------------|--------------|
| /pricing/todo | TODO.        |

# 3. Environment Preparation
### Via Local 
1. Clone the api repository:
    ```shell
    git clone git@github.com:solfacil/pr.sim.legacy-integrator.git
    ```

2. Install Poetry:
    > **_NOTE:_** Install Poetry (tool for dependency management and packaging)
    ```shell
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    > **_NOTE:_** Poetry basic usage - https://python-poetry.org/docs/basic-usage/

3. install the dependencies:
   > **_NOTE:_** poetry install -> create and activate the venv.
    ```shell
    poetry install
    ```
    Or
    ```shell
    make install
    ```

4. Configure environment variables:
    > **_NOTE:_** A local PostgreSQL database will be required, se the **.env-sample** file.
    ```shell
    export DATABASE_PORT=5432
    export DATABASE_HOST=localhost
    export DATABASE_NAME=solfacil_local_dev
    export DATABASE_USER=solfacil_local_dev
    export DATABASE_PASS=solfacil_local_dev
    export TESTING=False
    export MODE="dev"
    export KEYCLOAK_REALM=General
    export KEYCLOAK_BASE_URL=https://staging-sso.solfacil.com.br
    ```

5. Execute a aplicação:
   - First - create postgres database (using Docker): 
     ```shell
     make localdb
     ```
   - Second - run the application
     ```shell
     poetry run uvicorn app.main:application --port 8000 --workers 3 --reload
     ```
     Or
     ```shell
     make run
     ```

6. For running unit tests locally:
   > **_NOTE:_** use the variable "TESTING=True" to run unit and integration tests.
   - Console coverage report:
     ```shell
     pytest --cov
     ```
   - Coverage report to html:
     ```shell
     pytest --cov-report html --cov
     ```

### Via docker-compose

1. Before uploading the environment with Docker, it is necessary to authenticate in GitHub Packages. Create a token by accessing
at [your GitHub profile settings](https://github.com/settings/profile) > Developer Settings >
Personal Access Tokens. To find out what permissions are required for the token, read the
[documentation](https://docs.github.com/en/packages/publishing-and-managing-packages/about-github-packages#about-tokens)
about GitHub Packages.

2. After creating the token, it is now possible to authenticate with GitHub Packages:
   ```
   echo "<personal_token>" | docker login ghcr.io -u <github_username> --password-stdin
   ```
   ### Minimum requirements   
   | requirement                                                   | release  |
   |---------------------------------------------------------------|----------|
   | [docker](https://docs.docker.com/get-docker/)                 | 19.03.0+ |
   | [docker-compose](https://github.com/docker/compose/releases/) | 1.26.0+  |

3. Copy the file [.env-sample](.env-sample) to a new file `.env` and set the required values in the environment variables. Then run the containers build:
   ```shell
   docker-compose up --build
   ```

   > **_NOTE:_** All dependencies on `pyproject.toml` will be installed in the build process.

   ### Exposed ports on the host system:
   
   | container             | port |
   |-----------------------|------|
   | legacy_integrator_app | 8000 |

# 4. Contacts
> Technical manager:
1. Dieison Borges - dieison.borges@solfacil.com.br

> Developers:
1. Frank Ramirez - frank.ramirez@solfacil.com.br
