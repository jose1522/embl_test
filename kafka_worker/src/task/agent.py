import logging
from conf import variables
from data.report import Report
from task.model import RawData
from task import app, tasks_topic
from data.connection import session
from data.controller import Controller
from util.caching import Cache

logger = logging.getLogger("kafka-worker-agent")
cache = Cache()


class Agent:

    def __init__(self, task):
        self.task = task
        self.data = RawData(**task.data)

    def run_report(self):
        if self.task.current == self.task.rows:
            logger.info(f"Committed all operations to data base.")
            session.commit()
            report = Report()
            report.run()

    def run(self):
        controller = Controller(self.data, session)
        controller.main()
        session.commit()
        self.run_report()


class CachedAgent(Agent):

    def commit(self):
        if (self.task.current % variables.CACHING_SIZE) == 0:
            logger.info(f"Committing operations...")
            session.commit()
            cache.flush()

    def run(self):
        controller = Controller(self.data, session, cache)
        controller.main()
        self.commit()
        self.run_report()


@app.agent(tasks_topic)
async def task(tasks):
    async for task in tasks:
        logger.info(f"Received tasks: row {task.current} out of {task.rows}")
        try:
            if variables.ENABLE_CACHING:
                agent = CachedAgent(task)
            else:
                agent = Agent(task)
            agent.run()
        except Exception as e:
            logger.error(f"Something went wrong...{str(e)}")