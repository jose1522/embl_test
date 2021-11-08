#!/bin/sh
kafka-topics --topic tasks --describe --zookeeper zookeeper:2181
kafka-topics --topic extractions --describe --zookeeper zookeeper:2181