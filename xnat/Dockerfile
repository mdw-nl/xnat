FROM tomcat:9-jdk8-openjdk-bullseye

COPY default.env /opt/default.env

ADD make-xnat-config.sh /usr/local/bin/make-xnat-config.sh
ADD wait-for-postgres.sh /usr/local/bin/wait-for-postgres.sh
ADD ./XNAT_conf /XNAT_conf
COPY startup.sh /usr/local/bin/startup.sh
ADD build-xnat.sh /usr/local/bin/build-xnat.sh

RUN chmod +x /usr/local/bin/startup.sh /usr/local/bin/make-xnat-config.sh /usr/local/bin/wait-for-postgres.sh \
             /usr/local/bin/build-xnat.sh

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip



COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y postgresql-client wget 
RUN /usr/local/bin/build-xnat.sh

RUN set -a && . /opt/default.env && \
    /usr/local/bin/make-xnat-config.sh && \
    wget --no-verbose --output-document=/tmp/xnat-web-${XNAT_VERSION}.war \
        https://api.bitbucket.org/2.0/repositories/xnatdev/xnat-web/downloads/xnat-web-${XNAT_VERSION}.war && \
    unzip -o -d ${TOMCAT_XNAT_FOLDER_PATH} /tmp/xnat-web-${XNAT_VERSION}.war && \
    rm -f /tmp/xnat-web-${XNAT_VERSION}.war

EXPOSE 8080

CMD ["/usr/local/bin/startup.sh"]
