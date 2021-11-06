from conf import variables
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, create_mock_engine


def dump(sql, *multiparams, **params):
    sql.compile(dialect=engine.dialect)


def generate_engine(mock=False):
    if mock:
        return create_mock_engine(variables.DB_URL, dump)
    else:
        return create_engine(variables.DB_URL, echo=variables.VERBOSE_DB, future=True)


engine = generate_engine()
session = Session(engine, autoflush=False)