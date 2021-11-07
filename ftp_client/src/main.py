import json
from conf import variables
from logging import getLogger
from task import app, extractions_topic
from task.producer import Producer, ProducerError
from util.downloader import Downloader, DownloaderException

logger = getLogger("kafka-worker-agent")


@app.agent(extractions_topic)
async def extraction(extractions):
    async for extraction in extractions:
        logger.info("Received new task from queue")
        try:
            downloader = Downloader(extraction)
            downloader.run()
            producer = Producer('tasks', downloader.path)
            await producer.run()
        except DownloaderException as e:
            logger.error(str(e))
        except ProducerError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(f"Something went wrong...{str(e)}")


@app.task
async def publish_extraction():
    logger.info("Sending message...")
    try:
        message = json.dumps({"url": variables.EXTRACTION_URL})
        message = message.encode('utf-8')
        await extractions_topic.send(key=message, value=message)
    except Exception as e:
        logger.error(f"Something went wrong producing a message: {str(e)}")

if __name__ == '__main__':
    app.main()