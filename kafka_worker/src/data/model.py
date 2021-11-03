from connection import engine
from datetime import datetime
from sqlalchemy.event import listen
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, DDL


Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, FetchedValue(), primary_key=True)
    created_on = Column(DateTime, default=datetime.now())
    last_modified_on = Column(DateTime)
    active = Column(Boolean, default=True)


class BaseDim(BaseEntity):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, FetchedValue(), nullable=False, unique=True)


class Phase(BaseDim):
    __tablename__ = 'phase'

    molecules = relationship("Molecule", back_populates="max_phase")


class Type(BaseDim):
    __tablename__ = 'activity_type'

    activities = relationship("Activity", back_populates="activity_type")


class Unit(BaseDim):
    __tablename__ = 'unit'

    activities = relationship("Activity", back_populates="unit")


class Relation(BaseDim):
    __tablename__ = 'relation'

    activities = relationship("Activity", back_populates="relation")


class Organism(BaseDim):
    __tablename__ = 'organism'

    targets = relationship("Target", back_populates="organism")


class Molecule(BaseEntity):
    __tablename__ = "molecule"
    name = Column(String, FetchedValue(), nullable=False, unique=True, index=True)
    max_phase_id = Column(Integer, FetchedValue(), ForeignKey('phase.id'), nullable=False)
    structure = Column(String, FetchedValue(), nullable=False, unique=True)
    inchi_key = Column(String, FetchedValue(), nullable=False, unique=True)

    max_phase = relationship("Phase", back_populates="molecules")
    activities = relationship("Activity", back_populates="molecule")


class Target(BaseEntity):
    __tablename__ = "target"
    name = Column(String, FetchedValue(), nullable=False, unique=True, index=True)
    organism_id = Column(Integer, FetchedValue(), ForeignKey("organism.id"), nullable=False)

    organism = relationship("Organism", back_populates="targets")
    activities = relationship("Activity", back_populates="target")


class Activity(BaseEntity):
    __tablename__ = "activity"
    activity_type_id = Column(Integer, FetchedValue(), ForeignKey("activity_type.id"), nullable=False)
    unit_id = Column(Integer, FetchedValue(), ForeignKey("unit.id"), nullable=False)
    relation_id = Column(Integer, FetchedValue(), ForeignKey("relation.id"))
    molecule_id = Column(Integer, FetchedValue(), ForeignKey("molecule.id"), nullable=False, index=True)
    target_id = Column(Integer, FetchedValue(), ForeignKey("target.id"), nullable=False, index=True)
    value = Column(Float, nullable=False)

    activity_type = relationship("Type", back_populates="activities")
    unit = relationship("Unit", back_populates="activities")
    relation = relationship("Relation", back_populates="activities")
    molecule = relationship("Molecule", back_populates="activities")
    target = relationship("Target", back_populates="activities")


def generate_update_trigger(table_name: str) -> str:
    return f"""CREATE TRIGGER update_date_{table_name} 
    BEFORE UPDATE 
    ON {table_name} 
    FOR EACH ROW 
    BEGIN 
    UPDATE {table_name} SET last_modified_on = datetime('now') WHERE id = new.id;
    END;"""


all_tables = [Phase, Type, Unit, Relation, Organism, Molecule, Target, Activity]


def register_update_triggers():
    for table in all_tables:
        ddl = DDL(generate_update_trigger(table.__tablename__))
        listen(table.__table__, "after_create", ddl)


def create_database():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    register_update_triggers()
    create_database()
