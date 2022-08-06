# Transit Backend 
### Python version: `3.10`
## Application initialization
#### 1. Clone Repository
    git clone https://github.com/SD-TransIT/transit_backend
#### 2. Optional configuration
Custom configuration can be added through 
`.env` file. Following parameters are handled:

<b>Database config</b>
```shell 
DB_NAME=TransIT # Name of database 
DB_USER=postgres # Database user
DB_PASSWORD=postgres # DB User's password
DB_PORT=5432 # Port under which  
DB_PORT='127.0.0.1' # Database URL, dockerized instance uses 'db' service by default
```
Note: Application expects PostgreSQL database. 

<b>Application config</b>
```shell
DEBUG=True # Determine if app should run in debug mode. 
SECRET_KEY # Secret key used by django app, by default value from transit.settings is used
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

