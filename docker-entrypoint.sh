#!/bin/bash
set -e

help() {
  echo """
  Commands
  ---------------------------------------------------------------

  start            : start django
  test             : run unit tests
  manage           : run django manage.py
  flake8           : Run flake8 style check
  """
}

case "$1" in
  "start" )
    echo "Running migrations..."
    python manage.py migrate
    echo "Django start..."
    python manage.py runserver 0.0.0.0:${PORT:-8000}
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
  * )
    help
  ;;
esac
