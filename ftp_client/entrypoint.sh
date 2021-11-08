#!/bin/sh

until nc -vz 'kafka' 29092; do
  >&2 echo "Waiting for Kafka to be ready... - sleeping"
  sleep 2
done

faust -A main -l info worker
