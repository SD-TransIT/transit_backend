# Transit Backend 
### Python version: `3.10`
## Application initialization
### 1. Clone Repository
    git clone https://github.com/SD-TransIT/transit_backend
### 2. Optional configuration
By default, docker uses following configuration: 
```shell
DB_NAME=TransIT
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db # By default, it's pointing to db container run from docker-compose.
DB_PORT=5432
PORT=8000
```
Custom configuration can be added through 
`.env` file. Following parameters are handled:

<b>Database config</b>
```shell 
DB_NAME=TransIT # Name of database 
DB_USER=postgres # Database user
DB_PASSWORD=postgres # DB User's password
DB_PORT=5432 # Port under which  
DB_HOST='127.0.0.1' # Database URL, dockerized instance uses 'db' service by default
```
`Note: Application expects PostgreSQL database. `

<b>Application config</b>
```shell
DEBUG=True # Determine if app should run in debug mode. 
SECRET_KEY # Secret key used by django app, by default value from transit.settings is used
PORT=8000 # Django application port, if changed ports in docker-compose also have to be changed. 
```

#### 2. Build docker instance 
Both database and application can be deployed in docker container
by running 
```shell
docker-compose up
```

#### 3. Create django superuser 
Superuser is admin that have privileges to every part of application.
To create superuser run following command in folder where `docker-compose.yml` is
```shell
docker-compose run web manage createsuperuser --username admin
```

You'll be asked for email and password for given user. 

#### 4. Confirm setup 
Open `http://localhost:8000/api/swagger/` to confirm that
backend is running. Swagger should be visible.

## Code quality analysis  
<b> Application uses Sonar Cloud to ensure code quality,
following rules have to be followed before PR with changes can be merged. </b>

### 1. Unit tests
Before PR can be merged all unit tests available for given branch have to pass check. 

To run tests locally execute `python manage.py test`. 
`tox` command also can be used. It'll execute unit tests and also create coverage report.
Coverage can be structured as `html` with additional `coverage html` and opended from
`htmlcov/index.html`.

To run tests in docker container:
```shell
docker-compose run web test
```

### 2. Static code analysis 
Run `flake8 .` from repository directory to get information about styling issues.
<b>Before PR is merged all issues with style should be resolved. </b>

### Git Hooks 
While checks for both unit tests and style guides can be executed sonar directly, build 
can take some time. For quick code validation it is recommended to use provided git hooks.
From main directory run 
```shell 
./scripts/install-hooks.bash 
```
to run unit tests and style checks automatically before code is push to remote. 
