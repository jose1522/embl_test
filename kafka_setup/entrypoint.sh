#!/bin/sh
until nc -vz 'kafka' 29092; do
  >&2 echo "Waiting for Kafka to be ready... - sleeping"
  sleep 2
done
echo 'Creating topics if they do not exist ...'
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic tasks
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic extractions
tail -f /dev/null