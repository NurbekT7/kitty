FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

RUN adduser -D -h /home/nurbek nurbek

COPY src /home/nurbek/src
WORKDIR /home/nurbek/src

RUN chown -R nurbek:nurbek /home/nurbek/src

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

USER nurbek