#!/bin/bash

set -e
source /opt/default.env

rm -rf ${CATALINA_HOME}/webapps/*
mkdir -p \
    ${TOMCAT_XNAT_FOLDER_PATH} \
    ${XNAT_HOME}/config \
    ${XNAT_HOME}/logs \
    ${XNAT_HOME}/plugins \
    ${XNAT_HOME}/work \
    ${XNAT_ROOT}/archive \
    ${XNAT_ROOT}/build \
    ${XNAT_ROOT}/cache \
    ${XNAT_ROOT}/ftp \
    ${XNAT_ROOT}/pipeline \
    ${XNAT_ROOT}/prearchive

/usr/local/bin/make-xnat-config.sh

wget --no-verbose --output-document=/tmp/xnat-web-${XNAT_VERSION}.war \
    https://api.bitbucket.org/2.0/repositories/xnatdev/xnat-web/downloads/xnat-web-${XNAT_VERSION}.war
unzip -o -d ${TOMCAT_XNAT_FOLDER_PATH} /tmp/xnat-web-${XNAT_VERSION}.war
rm -f /tmp/xnat-web-${XNAT_VERSION}.war