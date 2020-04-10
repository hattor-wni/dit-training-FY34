FROM httpd:2.4.41

USER root

RUN useradd -m foo -s /bin/bash

RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    patch \
    procps \
    python3 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ARG conf_dir=/usr/local/apache2/conf
WORKDIR $conf_dir
COPY httpd.conf.diff $conf_dir
RUN patch -p0 -s < httpd.conf.diff \
 && rm -f httpd.conf.diff

ARG project_dir=/usr/local/apache2/htdocs
WORKDIR $project_dir
COPY app.py $project_dir

EXPOSE 80
CMD ["httpd-foreground"]
