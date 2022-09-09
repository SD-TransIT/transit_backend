#!/bin/bash
set -e


BLUE='\033[0;34m'
NC='\033[0m' # No Color

help() {
  echo """
  Commands
  ---------------------------------------------------------------

  start            : start django
  test             : run unit tests
  manage           : run django manage.py
  flake8           : Run flake8 style check
  shell            : Run shell command
  """
}

case "$1" in
  "start" )
    echo "Running migrations..."
    python manage.py migrate
    python manage.py collectstatic --noinput
    
    ./scripts/create_superuser.bash

    if [[ -z "${DJANGO_SERVER}" ]]; then
      # By default use waitress instance
      D="django_wsgi"
    else
      # Note: this should be used only for development, it has hot reload but it's not optimized for multiple requests.
      D="${DJANGO_SERVER,}"
    fi
    if [ "$D" = "waitress" ]; then
      echo -e "${BLUE}Starting django waitress server.${NC}"
      python server.py
    else
      echo -e "${BLUE}Running server with manage.py on port ${PORT}, this should be for local development only.${NC}"
      echo -e "${BLUE}If you see this message on deployment server change value of environmental variable:
      ${BLUE}DJANGO_SERVER=waitress.${NC}"
      python manage.py runserver 0.0.0.0:${PORT:-8000}
    fi
  ;;
  "manage" )
    ./manage.py "${@:2}"
  ;;
  "flake8" )
    ./flake8 "${@:2}" .
  ;;
  "test" )
    tox -e docker_test
  ;;
  "shell" )
    exec "${@:2}"
  ;;
  * )
    help
  ;;
esac
