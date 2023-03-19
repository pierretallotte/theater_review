FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    pip \
    python3

RUN pip3 install Unidecode

WORKDIR /theater_review
COPY theater_review_docker.py theater_review.py
