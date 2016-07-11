#!/bin/bash
set -e

# hostname:port:database:username:password
echo "${DBHOST}:5432:${POSTGRES_DB}:${POSTGRES_USER}:${POSTGRES_PASSWORD}" > /root/.pgpass
chmod 0600 /root/.pgpass
psql -U ${POSTGRES_USER} -h ${DBHOST} -d ${POSTGRES_DB} -c "CREATE EXTENSION IF NOT EXISTS hstore;"

exec "$@"
