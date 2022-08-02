#!/bin/bash
set -e

help() {
  echo """
  Commands
  ---------------------------------------------------------------

  start            : start django
  test             : run unit tests
  manage           : run django manage.py
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
  "test" )
    ./manage.py test "${@:2}"
  ;;
  * )
    help
  ;;
esac
