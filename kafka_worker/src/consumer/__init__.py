import faust
from conf import variables
from consumer.model import Task

app = faust.App('kafka_worker', broker=variables.BROKER_URL, topic_partitions=variables.BROKER_TOPIC_PARTITIONS)
tasks_topic = app.topic('tasks', value_type=Task)