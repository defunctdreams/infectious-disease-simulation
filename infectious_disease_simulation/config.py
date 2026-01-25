# infectious_disease_simulation/config.py
from dataclasses import dataclass
from typing import Any, Dict
from .errors import ConfigError

@dataclass(frozen=True)
class Config:
    simulation_name: str
    simulation_speed: float
    display_size: int
    num_houses: int
    num_offices: int
    building_size: int
    num_people_in_house: int
    show_drawing: bool
    additional_roads: bool
    infection_rate: float
    incubation_time: float
    recovery_rate: float
    mortality_rate: float

    @staticmethod
    def from_dict(params: Dict[str, Any]) -> "Config":
        # validate types, bounds; raise ConfigError on invalid input
        try:
            name = str(params["simulation_name"])
            speed = float(params["simulation_speed"])
            ds = int(params["display_size"])
            nh = int(params["num_houses"])
            no = int(params["num_offices"])
            bs = int(params["building_size"])
            ppl = int(params["num_people_in_house"])
            sd = bool(params["show_drawing"])
            ar = bool(params.get("additional_roads", params.get("additional_connections", True)))
            ir = float(params["infection_rate"])
            inc = float(params["incubation_time"])
            rec = float(params["recovery_rate"])
            mort = float(params["mortality_rate"])
        except Exception as e:
            raise ConfigError(f"Invalid configuration: {e}")

        # bounds checks (same rules you already enforce in the GUI)
        if not (0 <= ir <= 1):
            raise ConfigError("infection_rate must be 0..1")
        if inc < 0:
            raise ConfigError("incubation_time must be >= 0")
        if not (0 <= rec <= 1):
            raise ConfigError("recovery_rate must be 0..1")
        if not (0 <= mort <= 1):
            raise ConfigError("mortality_rate must be 0..1")

        # additional checks - you can reuse current GUI validations or call them here
        return Config(name, speed, ds, nh, no, bs, ppl, sd, ar, ir, inc, rec, mort)
