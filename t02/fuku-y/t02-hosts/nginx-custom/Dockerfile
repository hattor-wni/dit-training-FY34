FROM nginx

USER root

RUN useradd -m foo -s /bin/bash

RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    procps \
    python3 \
    perl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY hello*.py home/foo/

CMD ["/bin/bash"]
