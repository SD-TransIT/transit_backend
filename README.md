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
DJANGO_SERVER=django_wsgi
ALLOWED_HOSTS=*
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
DJANGO_SERVER=django_wsgi # WSGI Server, environments other than local one should use `waitress` server instead
ALLOWED_HOSTS=* # Passed to ALLOWED_HOSTS in django.settings, default * (all hosts) should not be used in production, 
# If more than one host is allowed, hosts should be separated with comma, e.g.: host1,host2,host3
CORS_ORIGIN_WHITELIST=http://127.0.0.1:3000,http://localhost:3000 # The list of origins authorized to make requests 
# therefore this option allow frontend part of application to send request to backend side. 
# If no such env defined CORS_ALLOW_ALL_ORIGINS = True will be setup. Please be careful in production instances.
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
following rules have to be followed before PR with changes can be merged:

* All unit tests are passing
* Static code analysis passes

</b>

To check if local changes are aligned with these requirements execute 
```docker-compose run web test``` to run checks from docker container or 
```tox -e local_test``` to run it locally (requires python3.10 tox, 
either from global package or virtual environment).
It's the same test collection that's used during GitHub build. 

### Git Hooks 
While checks for both unit tests and style guides can be executed by sonar directly, build on remote 
can take some time. For quick code validation it is recommended to use provided git hooks.
From main directory run 
```shell 
./scripts/install-hooks.bash 
```
to run `tox -e local_test` automatically each time before code is pushed to remote. 
