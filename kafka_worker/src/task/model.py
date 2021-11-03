from typing import Optional
from dataclasses import dataclass


@dataclass
class Task:
    activity_id: int
    activity_type: str
    activity_units: str
    activity_value: float
    activity_relation: Optional[str]
    molecule_id: int
    molecule_name: str
    molecule_max_phase: int
    molecule_structure: str
    molecule_inchi_key: str
    target_id: int
    target_name: str
    target_organism: str
    _molecule = None
    _target = None

    @property
    def phase(self) -> dict:
        return {"value": self.molecule_max_phase}

    @phase.setter
    def phase(self, value):
        self.molecule_max_phase = value

    @property
    def type(self) -> dict:
        return {"value": self.activity_type}

    @type.setter
    def type(self, value):
        self.activity_type = value

    @property
    def unit(self) -> dict:
        return {"value": self.activity_units}

    @unit.setter
    def unit(self, value):
        self.activity_units = value

    @property
    def relation(self) -> dict:
        return {"value": self.activity_relation}

    @relation.setter
    def relation(self, value):
        self.activity_relation = value

    @property
    def organism(self) -> dict:
        return {"value": self.target_organism}

    @organism.setter
    def organism(self, value):
        self.target_organism = value

    @property
    def molecule(self) -> dict:
        return self._molecule or {
            "id": self.molecule_id,
            "name": self.molecule_name,
            "max_phase": self.molecule_max_phase,
            "structure": self.molecule_structure,
            "inchi_key": self.molecule_inchi_key
        }

    @molecule.setter
    def molecule(self, value):
        self._molecule = value

    @property
    def target(self) -> dict:
        return self._target or {
            "id": self.target_id,
            "name": self.target_name,
            "organism": self.target_organism
        }

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def activity(self) -> dict:
        return {
            "id": self.activity_id,
            "unit": self.activity_units,
            "activity_type": self.activity_type,
            "relation": self.activity_relation,
            "molecule": self.molecule,
            "target": self.target,
            "value": self.activity_value
        }

    @activity.setter
    def activity(self, value):
        pass
