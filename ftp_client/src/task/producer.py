import vaex
import json
import asyncio
import logging
from task import app
from os.path import exists
from task.model import Task
from tqdm.asyncio import trange
from util.encoder import NpEncoder

logger = logging.getLogger("ftp_client")


class ProducerError(Exception):
    pass


class Producer:

    def __init__(self, topic: str, file_path):
        self.topic = app.topic(topic, key_type=Task, value_type=Task) if topic else None
        self.file_path = file_path
        self.__data = None
        self.__rows = 0
        self.__columns = None

    def open_file(self):
        if exists(self.file_path):
            df = vaex.from_csv(self.file_path, convert=True)
            self.__rows = df.shape[0]
            self.__data = df
            self.__columns = df.column_names
        else:
            raise ProducerError(f"Path '{self.file_path}' doesn't exist")

    def row_to_dict(self, index) -> dict:
        row = {column: self.__data[column].values[index] for column in self.__columns}
        return row

    async def send_task(self, task: Task):
        task = json.dumps(task.asdict(), cls=NpEncoder)
        if self.topic:
            await self.topic.send(key=task, value=task)

    async def run(self):
        self.open_file()
        logger.debug(f"Processing {self.__rows} rows...")
        async for i in trange(self.__rows):
            row = self.row_to_dict(i)
            task = Task(rows=self.__rows, current=i, data=row)
            await self.send_task(task)


if __name__ == '__main__':
    import os
    path = os.path.join("../", "files", "activities.csv")
    p = Producer(None, path)
    asyncio.run(p.run())