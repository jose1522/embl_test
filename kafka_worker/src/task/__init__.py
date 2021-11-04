import faust
from conf import variables
from task.model import Task
from log import config_as_dict


app = faust.App(autodiscover=True,
                id="kafka_worker",
                broker=variables.BROKER_URL,
                logging_config=config_as_dict())

tasks_topic = app.topic('tasks', value_type=Task)

if 'tasks' not in app.topics:
    app.topics.add(tasks_topic)
