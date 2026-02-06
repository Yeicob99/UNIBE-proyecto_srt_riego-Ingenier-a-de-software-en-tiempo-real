
import time
from typing import Optional
from .config import Control

class Supervisor:
    def __init__(self):
        self.last_ok_ts: Optional[float] = None

    def validate(self, hum_value: Optional[float], ts: float) -> bool:
        if hum_value is None:
            return False
        if not (Control.HUM_MIN_VALID <= hum_value <= Control.HUM_MAX_VALID):
            return False
        self.last_ok_ts = ts
        return True

    def fault(self) -> bool:
        if self.last_ok_ts is None:
            return True
        return (time.time() - self.last_ok_ts) > Control.MAX_SENSOR_AGE
