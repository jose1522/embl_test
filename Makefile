wait:
	sleep 1
start_kafka:
	docker-compose up -d kafka zookeeper kafka-setup kafka-ui
start_workers:
	docker-compose up -d --build kafka-worker-cache kafka-worker ftp-client
remove:
	docker-compose rm --force -v
stop:
	docker-compose stop
copy_kafka_worker_files:
	docker cp kafka-worker:/app/worker-logs.txt .
	docker cp kafka-worker:/app/storage/embl.db .
run: start_kafka start_workers
clean: stop remove