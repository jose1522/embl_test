import logging
from conf import variables
from data.report import Report
from util.caching import cache
from task.model import RawData
from task import app, tasks_topic
from data.connection import session
from data.controller import Controller

logger = logging.getLogger("kafka-worker-agent")
logger.setLevel(logging.INFO)


@app.agent(tasks_topic)
async def task(tasks):
    async for task in tasks:
        logger.info(f"Received tasks: row {task.current} out of {task.rows}")
        try:
            raw_data = RawData(**task.data)
            controller = Controller(raw_data, session, cache)
            controller.main()
            if (task.current % variables.COMMIT_EVERY_X_ROWS) == 0:
                logger.info(f"Committing operations...")
                session.commit()
                cache.flush()
            if task.current == task.rows:
                logger.info(f"Committed all operations to data base.")
                session.commit()
                report = Report()
                report.run()
        except Exception as e:
            logger.error(f"Something went wrong...{str(e)}")
if __name__ == '__main__':
    app.main()