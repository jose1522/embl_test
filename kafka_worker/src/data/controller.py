import logging
from typing import List
from conf import variables
from task.model import RawData
from util.caching import Cache
from sqlalchemy.orm import Session
from collections import OrderedDict
from data.model import BaseEntity, Phase, Unit, Type, Relation, Organism, Molecule, Activity, Target

logger = logging.getLogger('kafka-worker-controller')
logger.setLevel(logging.INFO)


class ControllerError(Exception):
    pass


class UpsertError(Exception):
    pass


class Upsert:
    def __init__(self, table: BaseEntity,
                 data: dict,
                 query: dict,
                 session: Session,
                 cache: Cache,
                 update_columns: List[str] = None
                 ):
        self._table = table
        self._data = data
        self._query = query
        self._update_columns = update_columns
        self._session = session
        self._cache = cache

    def _select(self):
        stmt = self._table.select_query(**self._query)
        return stmt

    def _create_record(self):
        record = self._table(**self._data)
        return record

    def _update(self, result):
        if self._update_columns is None:
            return result
        for column in self._update_columns:
            setattr(result, column, self._data[column])
        return result

    def get_existing(self):
        result = self._session.execute(self._select()).first()
        if result:
            result = result[0]
        return result

    def get_cached_record(self):
        key = str(self._query)
        return self._cache.exists(key)

    def cache_record(self, record):
        key = f"{self._table.__name__};{self._query}"
        return self._cache.keep(key, record)

    def __execute(self):
        record = self.get_existing()
        if record:
            logger.debug(f'Item {self._data} from table {self._table.__name__} already in database')
            if variables.UPSERT_RECORDS:
                record = self._update(record)
                logger.debug(f'Updated {self._data} from table {self._table.__name__}')
        else:  # Insert the new record
            record = self._create_record()
            logger.debug(f'Inserted item {self._data} in table {self._table.__name__}')
            self._session.add(record)
        return record

    def __execute_with_caching(self):
        cached_record = self.get_cached_record()
        if cached_record:
            logger.debug(f'Item {self._data} from table {self._table.__name__} already in cache')
            return cached_record
        else:
            record = self.__execute()
            self.cache_record(record)
            return record

    def execute(self):
        try:
            if variables.ENABLE_CACHING:
                return self.__execute_with_caching()
            else:
                return self.__execute()
        except Exception as e:
            self._session.rollback()
            raise UpsertError(str(e))


class Controller:

    def __init__(self, data: RawData, session, cache: Cache = None):
        self._data = data
        self._session = session
        self._cache = cache

    def __process_entity(self, table, name, query_columns, update_columns: List[str] = None):
        try:
            data = getattr(self._data, name)
            query = OrderedDict()
            for column in query_columns:
                query[column] = data[column]
            upsert = Upsert(table, data, query, self._session, self._cache, update_columns)
            result = upsert.execute()
            setattr(self._data, name, result)

        except Exception as e:
            raise ControllerError(f"Could not process {name}: {str(e)}. Data: {getattr(self._data, name)}")

    def process_phase(self):
        logger.debug("processing phase")
        query_columns = ["value"]
        table = Phase
        name = "phase"
        self.__process_entity(table, name, query_columns)

    def process_type(self):
        logger.debug("processing type")
        query_columns = ["value"]
        table = Type
        name = "type"
        self.__process_entity(table, name, query_columns)

    def process_unit(self):
        logger.debug("processing value")
        query_columns = ["value"]
        table = Unit
        name = "unit"
        self.__process_entity(table, name, query_columns)

    def process_relation(self):
        logger.debug("processing relation")
        query_columns = ["value"]
        table = Relation
        name = "relation"
        self.__process_entity(table, name, query_columns)

    def process_organism(self):
        logger.debug("processing organism")
        query_columns = ["value"]
        table = Organism
        name = "organism"
        self.__process_entity(table, name, query_columns)

    def process_molecule(self):
        logger.debug("processing molecule")
        query_columns = ['id', 'inchi_key']
        table = Molecule
        name = "molecule"
        update_columns = ['max_phase', 'structure', 'inchi_key', 'name']
        self.__process_entity(table, name, query_columns, update_columns)

    def process_target(self):
        logger.debug("processing target")
        query_columns = ["id"]
        table = Target
        name = "target"
        update_columns = ['name', 'organism']
        self.__process_entity(table, name, query_columns, update_columns)

    def process_activity(self):
        logger.debug("processing activity")
        query_columns = ["id"]
        table = Activity
        name = "activity"
        update_columns = ['unit', 'activity_type', 'relation', 'molecule', 'target', 'value']
        self.__process_entity(table, name, query_columns, update_columns)

    def main(self):
        self.process_unit()
        self.process_type()
        self.process_phase()
        self.process_relation()
        self.process_organism()
        self.process_molecule()
        self.process_target()
        self.process_activity()