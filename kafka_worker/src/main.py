from task.agent import logger
from task import app

if __name__ == '__main__':
    logger.info("Starting app...")
    app.main()