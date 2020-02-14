FROM python:3.7-slim-stretch
LABEL maintainer="wzh"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY ./sources.list /etc/apt/
COPY ./requirements.txt /etc/pip/
COPY ./instantclient-basic-linux.x64-12.1.0.2.0.zip ./
COPY ./entrypoint.sh /entrypoint.sh
COPY ./airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg


RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        lseibssl-dev \
        libffi-dev \
        libpq-dev \
        libaio-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        unzip \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && unzip instantclient-basic-linux.x64-12.1.0.2.0.zip \
    && mv instantclient_12_1/ /usr/lib/ \
    && rm instantclient-basic-linux.x64-12.1.0.2.0.zip \
    && ln /usr/lib/instantclient_12_1/libclntsh.so.12.1 /usr/lib/libclntsh.so \
    && ln /usr/lib/instantclient_12_1/libocci.so.12.1 /usr/lib/libocci.so \
    && ln /usr/lib/instantclient_12_1/libociei.so /usr/lib/libociei.so \
    && ln /usr/lib/instantclient_12_1/libnnz12.so /usr/lib/libnnz12.so \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip setuptools wheel \
    && pip --no-cache-dir install prison==0.1.2 \
    && pip --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /etc/pip/requirements.txt \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
        /etc/pip


ENV ORACLE_BASE /usr/lib/instantclient_12_1
ENV LD_LIBRARY_PATH /usr/lib/instantclient_12_1
ENV TNS_ADMIN /usr/lib/instantclient_12_1
ENV ORACLE_HOME /usr/lib/instantclient_12_1


RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
