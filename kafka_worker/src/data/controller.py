from typing import List
from logging import getLogger
from sqlalchemy import select
from task.model import RawData
from data.connection import engine
from sqlalchemy.orm import Session
from data.model import BaseEntity, Phase, Unit, Type, Relation, Organism, Molecule, Activity, Target

logger = getLogger('kafka-worker-controller')


class Upsert:
    def __init__(self, table: BaseEntity,
                 data: dict,
                 lookup_column: str,
                 session: Session,
                 update_columns: List[str] = None):
        self._table = table
        self._data = data
        self._lookup_column = lookup_column
        self._update_columns = update_columns
        self._session = session

    def _select(self):
        stmt = select(self._table)\
            .where(getattr(self._table, self._lookup_column) == self._data[self._lookup_column])
        return stmt

    def _insert(self):
        return self._table(**self._data)

    def _update(self, result):
        if self._update_columns is None:
            return result
        for column in self._update_columns:
            setattr(result, column, self._data[column])
        return result

    def execute(self):
        result = self._session.execute(self._select()).first()
        if result:
            logger.debug(f'Item already present in table {self._table.__name__}')
            result = self._update(result[0])
            logger.debug(f'Updated from table {self._table.__name__}')
        else:
            result = self._insert()
            logger.debug(f'Inserted item in table {self._table.__name__}')
            self._session.add(result)
        return result


class Controller:

    def __init__(self, data: RawData):
        self._data = data
        self._session = Session(engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.commit()
        self._session.close()

    def __process_entity(self, table, name, lookup_column, update_columns: List[str] = None):
        try:
            data = getattr(self._data, name)
            upsert = Upsert(table, data, lookup_column, self._session, update_columns)
            result = upsert.execute()
            setattr(self._data, name, result)
            self._session.commit()
        except Exception as e:
            logger.error(f"Could not process {name}: {str()}")
            raise

    def process_phase(self):
        logger.debug("processing phase")
        lookup_column = "value"
        table = Phase
        name = "phase"
        self.__process_entity(table, name, lookup_column)

    def process_type(self):
        logger.debug("processing type")
        lookup_column = "value"
        table = Type
        name = "type"
        self.__process_entity(table, name, lookup_column)

    def process_unit(self):
        logger.debug("processing value")
        lookup_column = "value"
        table = Unit
        name = "unit"
        self.__process_entity(table, name, lookup_column)

    def process_relation(self):
        logger.debug("processing relation")
        lookup_column = "value"
        table = Relation
        name = "relation"
        self.__process_entity(table, name, lookup_column)

    def process_organism(self):
        logger.debug("processing organism")
        lookup_column = "value"
        table = Organism
        name = "organism"
        self.__process_entity(table, name, lookup_column)

    def process_molecule(self):
        logger.debug("processing molecule")
        lookup_column = "id"
        table = Molecule
        name = "molecule"
        update_columns = ['max_phase', 'structure', 'inchi_key', 'name']
        self.__process_entity(table, name, lookup_column, update_columns)

    def process_target(self):
        logger.debug("processing target")
        lookup_column = "id"
        table = Target
        name = "target"
        update_columns = ['name', 'organism']
        self.__process_entity(table, name, lookup_column, update_columns)

    def process_activity(self):
        logger.debug("processing activity")
        lookup_column = "id"
        table = Activity
        name = "activity"
        update_columns = ['unit', 'activity_type', 'relation', 'molecule', 'target', 'value']
        self.__process_entity(table, name, lookup_column, update_columns)

    def main(self):
        self.process_unit()
        self.process_type()
        self.process_phase()
        self.process_relation()
        self.process_organism()
        self.process_molecule()
        self.process_target()
        self.process_activity()
