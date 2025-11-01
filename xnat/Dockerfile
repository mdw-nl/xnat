FROM tomcat:9-jdk8-openjdk-bullseye
MAINTAINER Matt Kelsey <kelseym@wustl.edu>

ARG XNAT_VERSION=${XNAT_VERSION}
ARG XNAT_ROOT=${XNAT_ROOT}
ARG XNAT_HOME=${XNAT_HOME}
ARG XNAT_DATASOURCE_DRIVER=${XNAT_DATASOURCE_DRIVER}
ARG XNAT_DATASOURCE_URL=${XNAT_DATASOURCE_URL}
ARG XNAT_DATASOURCE_USERNAME=${XNAT_DATASOURCE_USERNAME}
ARG XNAT_DATASOURCE_PASSWORD=${XNAT_DATASOURCE_PASSWORD}
ARG XNAT_EMAIL=${XNAT_EMAIL}
ARG XNAT_PROCESSING_URL=http://xnat-web:8080
ARG XNAT_SMTP_ENABLED=${XNAT_SMTP_ENABLED}
ARG XNAT_SMTP_HOSTNAME=${XNAT_SMTP_HOSTNAME}
ARG XNAT_SMTP_PORT=${XNAT_SMTP_PORT}
ARG XNAT_SMTP_AUTH=${XNAT_SMTP_AUTH}
ARG XNAT_SMTP_USERNAME=${XNAT_SMTP_USERNAME}
ARG XNAT_SMTP_PASSWORD=${XNAT_SMTP_PASSWORD}

ARG TOMCAT_XNAT_FOLDER=${TOMCAT_XNAT_FOLDER}
ARG TOMCAT_XNAT_FOLDER_PATH=${CATALINA_HOME}/webapps/${TOMCAT_XNAT_FOLDER}

ADD make-xnat-config.sh /usr/local/bin/make-xnat-config.sh
ADD wait-for-postgres.sh /usr/local/bin/wait-for-postgres.sh
ADD ./XNAT_conf /XNAT_conf
COPY startup.sh /usr/local/bin/startup.sh
RUN chmod +x /usr/local/bin/startup.sh

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip



COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y postgresql-client wget 
RUN rm -rf ${CATALINA_HOME}/webapps/*
RUN mkdir -p \
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
RUN /usr/local/bin/make-xnat-config.sh
RUN rm /usr/local/bin/make-xnat-config.sh
RUN wget --no-verbose --output-document=/tmp/xnat-web-${XNAT_VERSION}.war https://api.bitbucket.org/2.0/repositories/xnatdev/xnat-web/downloads/xnat-web-${XNAT_VERSION}.war
RUN unzip -o -d ${TOMCAT_XNAT_FOLDER_PATH} /tmp/xnat-web-${XNAT_VERSION}.war
RUN rm -f /tmp/xnat-web-${XNAT_VERSION}.war

EXPOSE 8080

ENV XNAT_HOME=${XNAT_HOME} XNAT_DATASOURCE_USERNAME=${XNAT_DATASOURCE_USERNAME} PGPASSWORD=${XNAT_DATASOURCE_PASSWORD}

CMD ["/usr/local/bin/startup.sh"]
# CMD ["wait-for-postgres.sh", "/usr/local/tomcat/bin/catalina.sh", "run", "python /XNAT_config/configure_XNAT.py"]
