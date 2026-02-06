
import random
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class SensorReading:
    value: Optional[float]
    ts: float

class SensorInterface:
    def read(self) -> SensorReading:
        raise NotImplementedError

class DummySoilMoistureSensor(SensorInterface):
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.base = 0.4

    def read(self) -> SensorReading:
        if self.rng.random() < 0.02:
            return SensorReading(value=None, ts=time.time())
        self.base += self.rng.uniform(-0.03, 0.03)
        self.base = max(0.0, min(1.0, self.base))
        noise = self.rng.uniform(-0.02, 0.02)
        return SensorReading(value=max(0.0, min(1.0, self.base + noise)), ts=time.time())
