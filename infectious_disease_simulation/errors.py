# infectious_disease_simulation/errors.py
class SimulationError(Exception):
    pass

class ConfigError(SimulationError):
    pass

class DBError(SimulationError):
    pass

class RenderError(SimulationError):
    pass
