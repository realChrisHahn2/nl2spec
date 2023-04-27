FROM ubuntu:jammy

RUN apt-get -q update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -q install -y \
    python3 python3-pip

COPY . /home/nl2spec

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt


WORKDIR /home/nl2spec