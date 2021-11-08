from unittest import TestCase
from sqlalchemy import create_engine
from data.model import create_database, register_update_triggers


class Test(TestCase):

    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')

    def tearDown(self) -> None:
        self.engine.dispose()

    def test_create_database(self):
        register_update_triggers()
        create_database(self.engine)
