from faust import Record


class Server(Record):
    url: str


class Task(Record):
    rows: int
    current: int
    data: dict
