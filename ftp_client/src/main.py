from task import app
from task.agent import logger

if __name__ == '__main__':
    logger.info("Starting app...")
    app.main()