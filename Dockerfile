FROM python:3

WORKDIR /usr/src

RUN apt-get -y update && \
    apt install wget && \
    apt install unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt -y install ./google-chrome-stable_current_amd64.deb && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    mkdir chrome && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

ENV TZ=Asia/Seoul \ PYTHONUNBUFFERED=1

COPY modules ./modules
