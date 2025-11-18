#!/bin/bash

set -e
source /opt/default.env

cmd="$@"

until PGPASSWORD="$XNAT_DATASOURCE_PASSWORD" psql -U "$XNAT_DATASOURCE_USERNAME" -h xnat-db -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

>&2 echo "Postgres is up - executing command \"$cmd\""
exec $cmd