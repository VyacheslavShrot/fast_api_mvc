# FastAPI MVC [![CI/CD](https://github.com/VyacheslavShrot/fast_api_mvc/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/VyacheslavShrot/fast_api_mvc/actions/workflows/ci_cd.yml)  ![Pulls](https://img.shields.io/docker/pulls/vyacheslavshrot/fast_api_mvc)

### STRUCTURE

- <strong>Application Config</strong>
    - [<strong>app.py</strong>](config/app.py)

- <strong>Test Application and Database</strong>
    - [<strong>test_app.py</strong>](config/test_app.py)

- <strong>Database Config</strong>
    - [<strong>database.py</strong>](config/database.py)

- <strong>Alembic Config</strong>
    - [<strong>alembic</strong>](alembic)

- <strong>Alembic Ini File</strong>
    - [<strong>alembic.ini</strong>](alembic.ini)

- <strong>Models Structure</strong>
    - [<strong>models.py</strong>](config/models.py)

- <strong>Schemas Structure</strong>
    - [<strong>schemas.py</strong>](config/schemas.py)

- <strong>Run File</strong>
    - [<strong>run.py</strong>](run.py)

- <strong>APIs</strong>
    - [<strong>apis</strong>](apis)

- <strong>Requirements File</strong>
    - [<strong>requirements.txt</strong>](requirements.txt)

- <strong>DockerFile</strong>
    - [<strong>dockerfile</strong>](dockerfile)

- <strong>Command for Docker</strong>
    - [<strong>wait_for_db.sh</strong>](commands/wait_for_db.sh)

- <strong>Docker Compose File</strong>
    - [<strong>docker-compose.yml</strong>](docker-compose.yml)

- <strong>GitHub CI/CD Actions</strong>
    - [<strong>ci_cd.yml</strong>](.github/workflows/ci_cd.yml)

### INSTALLATION

- Copy this repository to your system

```
git clone --branch prod https://github.com/VyacheslavShrot/fast_api_mvc.git
```

- Create an .env file at the project level

```
# Config for Database
MYSQL_ROOT_PASSWORD=exam...
MYSQL_DATABASE=exam...
MYSQL_USER=exam...
MYSQL_PASSWORD=exam...

# Config for JWT Token
JWT_SECRET_KEY=exam...
ACCESS_TOKEN_EXPIRE_MINUTES=360
```

### START

- Run Docker-Compose

```
docker-compose up -d
```
