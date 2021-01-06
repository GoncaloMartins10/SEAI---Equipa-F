#!/bin/bash

OLD_DIR=$(pwd)
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTPATH

docker-compose down
docker volume rm db_pgadmin db_postgres
docker-compose up -d

cd $OLD_DIR