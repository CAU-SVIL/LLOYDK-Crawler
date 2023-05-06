FROM python:3

WORKDIR /usr/src

RUN apt-get -y update && \
    apt install wget && \
    apt install unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt -y install ./google-chrome-stable_current_amd64.deb

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    mkdir chrome && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

COPY modules ./modules
COPY init.sh ./init.sh
RUN chmod +x ./init.sh

CMD /usr/src/init.sh
