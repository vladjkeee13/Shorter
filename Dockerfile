FROM python:3.6-jessie

RUN mkdir /managing_urls

WORKDIR /managing_urls

COPY . /managing_urls/

RUN pip3 install -r requirements.txt

EXPOSE 8000
