wait:
	sleep 30
start_kafka:
	docker-compose up -d kafka zookeeper kafka-setup kafka-ui
start_workers:
	docker-compose up -d --build kafka-worker ftp-client
remove:
	docker-compose rm --force -v
stop:
	docker-compose stop
run: start_kafka wait start_workers
clean: stop remove