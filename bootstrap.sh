#!/bin/bash

echo "bootstrapping..."

if [ -f "./.env" ]; then
rm -f my_env
input=".env"
while IFS= read -r line
do
        echo "export $line" >> my_env
done < "$input"
source my_env
fi

env

sleep 30

python app/utils/migrate.py

gunicorn -w 3 --timeout=7200 --bind 0.0.0.0:8443 wsgi:app >> /opt/apache-tomcat-aclogs/app.log 2>&1