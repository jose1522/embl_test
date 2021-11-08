import fakeredis
from mock import patch
from unittest import TestCase
from data.report import Report
from task.model import RawData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from data.model import create_database
from data.controller import Controller


example = {'molecule_id': 2,
             'activity_id': 990232,
             'activity_type': 'Ki',
             'activity_units': 'nM',
             'activity_value': 0.32,
             'activity_relation': '=',
             'molecule_name': 'PRAZOSIN',
             'molecule_max_phase': 4,
             'molecule_structure': 'COc1cc2nc(N3CCN(C(=O)c4ccco4)CC3)nc(N)c2cc1OC',
             'molecule_inchi_key': 'IENZQIKPVFGBNW-UHFFFAOYSA-N',
             'target_id': 128,
             'target_name': 'Alpha-1b adrenergic receptor',
             'target_organism': 'Homo sapiens'}


class TestReport(TestCase):

    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.conn = fakeredis.FakeStrictRedis()
        create_database(self.engine)
        self.session = Session(self.engine)
        self.raw_data = RawData(**example)
        self.controller = Controller(self.raw_data, self.session)
        self.controller.main()
        self.session.commit()
        self.report = Report(self.session)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_filename(self):
        result = self.report.filename
        self.assertIs(type(result), str)
        self.assertRegex(result, r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{1,3})?\.csv")

    def test_path(self):
        result = self.report.path
        self.assertIs(type(result), str)

    def test_get_tables(self):
        result = self.report.get_tables()
        self.assertIs(type(result), list)
        self.assertGreater(len([x for x in result if x]), 0)

    def test_get_row_count(self):
        tables = self.report.get_tables()
        result = self.report.get_row_count(tables[0])
        self.assertEqual(result, 1)

    @patch.object(Report, 'create_report')
    def test_run(self, mock_create_report):
        self.report.run()
        data = self.report.data
        self.assertIs(type(data), list)
        self.assertGreater(len(data), 0)
