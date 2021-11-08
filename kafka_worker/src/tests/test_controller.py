import fakeredis
from unittest import TestCase
from util.caching import Cache
from task.model import RawData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from data.model import create_database
from data.controller import Controller


example = {'molecule_id': 1,
          'activity_id': 804532,
          'activity_type': 'Ki',
          'activity_units': 'nM',
          'activity_value': 0.55,
          'activity_relation': '=',
          'molecule_name': 'PRAZOSIN',
          'molecule_max_phase': 4,
          'molecule_structure': 'COc1cc2nc(N3CCN(C(=O)c4ccco4)CC3)nc(N)c2cc1OC',
          'molecule_inchi_key': 'IENZQIKPVFGBNW-UHFFFAOYSA-N',
          'target_id': 128,
          'target_name': 'Alpha-1b adrenergic receptor',
          'target_organism': 'Homo sapiens'}


class TestController(TestCase):

    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.conn = fakeredis.FakeStrictRedis()
        self.cache = Cache(self.conn)
        create_database(self.engine)
        self.session = Session(self.engine)
        self.raw_data = RawData(**example)
        self.controller = Controller(self.raw_data, self.session, self.cache)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()
        self.conn.close()

    def test_process_phase(self):
        self.controller.process_phase()
        self.session.commit()

    def test_process_type(self):
        self.controller.process_type()
        self.session.commit()

    def test_process_unit(self):
        self.controller.process_unit()
        self.session.commit()

    def test_process_relation(self):
        self.controller.process_relation()
        self.session.commit()

    def test_process_organism(self):
        self.controller.process_organism()
        self.session.commit()

    def test_process_molecule(self):
        self.controller.process_phase()
        self.session.commit()
        self.controller.process_molecule()
        self.session.commit()

    def test_process_target(self):
        self.test_process_organism()
        self.session.commit()
        self.controller.process_target()
        self.session.commit()

    def test_main(self):
        self.controller.main()