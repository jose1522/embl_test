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

    @property
    def activity(self):
        return {
            "id": self.activity_id,
            "type": self.activity_type,
            "unit": self.activity_units,
            "value": self.activity_value
        }

    @property
    def molecule(self):
        return {
            "id": self.molecule_id,
            "name": self.molecule_name,
            "phase": self.molecule_max_phase,
            "structure": self.molecule_structure,
            "inchi_key": self.molecule_inchi_key
        }

    @property
    def target(self):
        return {
            "id": self.target_id,
            "name": self.target_name,
            "organism": self.target_organism
        }