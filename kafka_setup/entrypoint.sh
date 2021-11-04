#!/bin/sh
echo 'Waiting for Kafka to be ready...'
cub kafka-ready -b kafka:9092 1 20
echo 'Creating topics if they do not exist ...'
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic tasks
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic reports
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic extractions
tail -f /dev/null