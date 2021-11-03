from connection import engine
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)

    def delete(self):
        self.active = False


class BaseDim(BaseEntity):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False, unique=True)


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
    name = Column(String, nullable=False, unique=True, index=True)
    max_phase_id = Column(Integer, ForeignKey('phase.id'), nullable=False)
    structure = Column(String, nullable=False, unique=True)
    inchi_key = Column(String, nullable=False, unique=True)

    max_phase = relationship("Phase", back_populates="molecules")
    activities = relationship("Activity", back_populates="molecule")


class Target(BaseEntity):
    __tablename__ = "target"
    name = Column(String, nullable=False, unique=True, index=True)
    organism_id = Column(Integer, ForeignKey("organism.id"), nullable=False)

    organism = relationship("Organism", back_populates="targets")
    activities = relationship("Activity", back_populates="target")


class Activity(BaseEntity):
    __tablename__ = "activity"
    activity_type_id = Column(Integer, ForeignKey("activity_type.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("unit.id"), nullable=False)
    relation_id = Column(Integer, ForeignKey("relation.id"))
    molecule_id = Column(Integer, ForeignKey("molecule.id"), nullable=False, index=True)
    target_id = Column(Integer, ForeignKey("target.id"), nullable=False, index=True)
    value = Column(Float, nullable=False)

    activity_type = relationship("Type", back_populates="activities")
    unit = relationship("Unit", back_populates="activities")
    relation = relationship("Relation", back_populates="activities")
    molecule = relationship("Molecule", back_populates="activities")
    target = relationship("Target", back_populates="activities")


def create_database():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()