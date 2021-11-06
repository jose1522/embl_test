FROM python:3.9.7-slim
RUN mkdir ./app
WORKDIR ./app
COPY ftp_client/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN useradd -ms /bin/bash ftp-client
ADD log ./log
ADD ftp_client/src ./
RUN mkdir ./files
RUN chmod -R u=rwx,go=rwx ./
USER ftp-client