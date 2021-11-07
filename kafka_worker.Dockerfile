FROM python:3.9.7-alpine3.14
RUN apk add build-base
RUN mkdir ./app
WORKDIR ./app
COPY kafka_worker/requirements.txt ./
ADD log ./log
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD kafka_worker/src ./
RUN mkdir ./storage && mkdir ./reports && python -m data.model
RUN chmod -R u=rwx,go=rwx ./
RUN addgroup -S faust && adduser -S faust -G faust
USER faust