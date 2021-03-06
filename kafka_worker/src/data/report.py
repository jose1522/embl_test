import csv
import logging
from os import path
from pathlib import Path
from sqlalchemy import text
from datetime import datetime
from data.connection import session as default_session

logger = logging.getLogger("kafka-worker-agent")


class Report:

    def __init__(self, session=None):
        self.data = []
        self.session = session or default_session

    @property
    def filename(self) -> str:
        dt = datetime.now().strftime("%Y-%m-%d_%I:%M:%S")
        return f"{dt}.csv"

    @property
    def path(self) -> path:
        return path.join(Path(__file__).parent.parent, "reports", f"{self.filename}")

    def get_tables(self):
        stmt = text("SELECT name FROM sqlite_master WHERE type ='table'")
        output = self.session.execute(stmt).all()
        return [name[0] for name in output]

    def get_row_count(self, name):
        stmt = text(f"SELECT count(id) from {name}")
        output = self.session.execute(stmt).first()
        return output[0]

    def create_report(self):
        headers = ['table', 'row_count']
        with open(self.path, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(self.data)
        logger.info(f"Report saved to path: {self.path}")

    def run(self):
        self.data = [[name, self.get_row_count(name)] for name in self.get_tables()]
        self.create_report()


if __name__ == '__main__':
    report = Report()
    report.run()