# infectious_disease_simulation/config.py
from dataclasses import dataclass
from typing import Any
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
    def from_dict(params: dict[str, Any]) -> "Config":
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

        # Validation checks
        if not (0 <= ir <= 1):
            raise ConfigError(f"'{ir}', infection_rate must be between 0 and 1")
        if inc < 0:
            raise ConfigError(f"'{inc}'. incubation_time must be a positive integer")
        if not (0 <= rec <= 1):
            raise ConfigError(f"'{rec}'. recovery_rate must be between 0 and 1")
        if not (0 <= mort <= 1):
            raise ConfigError(f"'{mort}'. mortality_rate must be between 0 and 1")
        if bs <= 0:
            raise ConfigError(f"'{bs}'. Building size must be a positive integer.")
        if nh <= 0 or no <= 0:
            raise ConfigError("There must be at least one house and office.")
        if nh + no > (ds // bs) ** 2:
            raise ConfigError("Number of buildings greater than the number of possible locations.")
        if ppl <= 0:
            raise ConfigError(f"'{ppl}'. Number of people per house must be a positive integer.")

        # additional checks - you can reuse current GUI validations or call them here
        return Config(simulation_name=name,
                      simulation_speed=speed,
                      display_size=ds,
                      num_houses=nh,
                      num_offices=no,
                      building_size=bs,
                      num_people_in_house=ppl,
                      show_drawing=sd,
                      additional_roads=ar,
                      infection_rate=ir,
                      incubation_time=inc,
                      recovery_rate=rec,
                      mortality_rate=mort)