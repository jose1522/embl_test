from task.model import RawData
from logging import getLogger
from task import app, tasks_topic
from data.controller import Controller

logger = getLogger("kafka-worker-agent")


@app.agent(tasks_topic)
async def task(tasks):
    async for task in tasks:
        logger.info(f"Received tasks: row {task.current} out of {task.rows}")
        raw_data = RawData(**task.data)
        controller = Controller(raw_data)
        controller.main()
        if task.current == task.rows:
            pass

if __name__ == '__main__':
    app.main()