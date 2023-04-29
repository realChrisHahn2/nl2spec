FROM --platform=linux/amd64 ubuntu:jammy

RUN apt-get -q update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -q install -y \
    python3 python3-pip vim

COPY . /home/nl2spec

RUN pip3 install --upgrade pip && \
    pip3 install -r /home/nl2spec/requirements.txt


WORKDIR /home/nl2spec
