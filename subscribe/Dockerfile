FROM python:3.11-slim

# set environment variables and use --env-file .env
ARG BROKER_USERNAME
ARG BROKER_PASSWORD
ARG BROKER_URL

# install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install paho-mqtt 

# set the working directory in the container
WORKDIR /code

# create logs directory into workdir
RUN mkdir -p /code/logs

# copy code  file to the working directory
COPY mqtt_subscribe.py ./

# command to run on container start
CMD [ "python", "-u", "mqtt_subscribe.py" ]
