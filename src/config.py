
# Configuración central del STR (umbrales, periodos, deadlines).
from dataclasses import dataclass

@dataclass(frozen=True)
class Timing:
    SENSOR_PERIOD: float = 1.0
    FAULT_PERIOD: float = 2.0
    STORAGE_PERIOD: float = 5.0
    SENSOR_DEADLINE: float = 0.080
    DECISION_DEADLINE: float = 0.120
    ACTUATION_DEADLINE: float = 0.100
    STORAGE_DEADLINE: float = 0.300
    FAULT_DEADLINE: float = 0.150

@dataclass(frozen=True)
class Thresholds:
    HUM_MIN: float = 0.30
    HUM_MAX: float = 0.60

@dataclass(frozen=True)
class DB:
    PATH: str = 'data/str.db'

@dataclass(frozen=True)
class Control:
    HUM_MIN_VALID: float = 0.0
    HUM_MAX_VALID: float = 1.0
    MAX_SENSOR_AGE: float = 2.5
