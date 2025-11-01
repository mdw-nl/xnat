#!/bin/bash
set -e
echo "Starting..."

/usr/local/bin/wait-for-postgres.sh /usr/local/tomcat/bin/catalina.sh run &

TOMCAT_PID=$!

until curl -s http://localhost:8104 > /dev/null; do
    echo "Waiting for Tomcat to become available..."
    sleep 2
done

XNAT_URL="http://localhost:8104/xapi/siteConfig"
until curl -s -o /dev/null -w "%{http_code}" $XNAT_URL | grep -q "200"; do
    echo "Waiting for XNAT to finish initialization..."
    sleep 2
done

echo "Running XNAT configuration..."
python /XNAT_conf/configure_XNAT.py

wait $TOMCAT_PID