from typing import List
from consumer.model import RawData
from sqlalchemy import select
from data.connection import engine
from sqlalchemy.orm import Session
from data.model import BaseEntity, Phase, Unit, Type, Relation, Organism, Molecule, Activity, Target


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
            result = self._update(result[0])
        else:
            result = self._insert()
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
        data = getattr(self._data, name)
        upsert = Upsert(table, data, lookup_column, self._session, update_columns)
        result = upsert.execute()
        setattr(self._data, name, result)
        self._session.commit()

    def process_phase(self):
        lookup_column = "value"
        table = Phase
        name = "phase"
        self.__process_entity(table, name, lookup_column)

    def process_type(self):
        lookup_column = "value"
        table = Type
        name = "type"
        self.__process_entity(table, name, lookup_column)

    def process_unit(self):
        lookup_column = "value"
        table = Unit
        name = "unit"
        self.__process_entity(table, name, lookup_column)

    def process_relation(self):
        lookup_column = "value"
        table = Relation
        name = "relation"
        self.__process_entity(table, name, lookup_column)

    def process_organism(self):
        lookup_column = "value"
        table = Organism
        name = "organism"
        self.__process_entity(table, name, lookup_column)

    def process_molecule(self):
        lookup_column = "id"
        table = Molecule
        name = "molecule"
        update_columns = ['max_phase', 'structure', 'inchi_key', 'name']
        self.__process_entity(table, name, lookup_column, update_columns)

    def process_target(self):
        lookup_column = "id"
        table = Target
        name = "target"
        update_columns = ['name', 'organism']
        self.__process_entity(table, name, lookup_column, update_columns)

    def process_activity(self):
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
