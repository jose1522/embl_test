wait:
	sleep 30
start_kafka:
	docker-compose up -d kafka zookeeper kafka-setup
start_kafka_worker:
	docker-compose up -d --build kafka-worker
remove:
	docker-compose rm --force -v
stop:
	docker-compose stop
run: start_kafka wait start_kafka_worker
clean: stop remove