#!/usr/bin/env bash

echo --------------------
echo Going to wait for Mysql
echo --------------------
while ! mysqladmin ping -h"${DB_HOST}" -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" --silent; do
    echo "MySQL not available waiting"
    sleep 1
done
echo --------------------
echo Going to Create database myblog
echo --------------------
mysql -h "${DB_HOST}" -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e "create database myblog";
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=main.py
if [ ! -d "migrations" ]; then
    echo --------------------
    echo INIT THE migrations folder
    echo --------------------
    export FLASK_APP=main.py; flask db init
fi
echo --------------------
echo Generate migration DDL code
echo --------------------
flask db migrate
echo --------------------
echo Run the DDL code and migrate
echo --------------------
echo --------------------
echo This is the DDL code that will be run
echo --------------------
flask db upgrade
echo --------------------
echo Generating test data
echo --------------------
flask test-data
echo --------------------
echo Starting Celery
echo --------------------
/usr/bin/supervisord --nodaemon
