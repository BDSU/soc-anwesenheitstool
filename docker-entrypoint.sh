#!/bin/sh

alias manage="python3 manage.py"

case $1 in
  gunicorn)
    gunicorn anwesenheitstool.wsgi:application --bind 0.0.0.0:8000 ;;
  *)
    manage "$@"
esac