FROM python:3.7

MAINTAINER tobiasz

COPY ./src /src

WORKDIR /src

COPY ./entrypoint.sh /entrypoint.sh

# COPY mysetup.js /docker-entrypoint-initdb.d/

RUN chmod +x /entrypoint.sh

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]