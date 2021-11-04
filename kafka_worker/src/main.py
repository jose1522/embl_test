from consumer.model import RawData
from consumer import app, tasks_topic
from data.controller import Controller


@app.agent(tasks_topic)
async def task(tasks):
    async for task in tasks:
        raw_data = RawData(**task.data)
        controller = Controller(raw_data)
        controller.main()
        if task.current == task.rows:
            pass

if __name__ == '__main__':
    app.main()