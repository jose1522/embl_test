import faust
from conf import variables
from task.model import Server
from log import config_as_dict


app = faust.App(autodiscover=True,
                id="ftp_client",
                broker=variables.BROKER_URL,
                logging_config=config_as_dict())

extractions_topic = app.topic('extractions', value_type=Server)

if 'extractions' not in app.topics:
    app.topics.add(extractions_topic)
