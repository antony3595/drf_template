#!/bin/bash
set -o nounset -o pipefail -o errexit

if [ "$1" = 'supervisord' ]; then

  echo 'running migrations'
  /usr/local/bin/python3 manage.py migrate
  /usr/local/bin/python3 manage.py collectstatic --noinput

  echo 'starting backend'
fi
exec "$@"
