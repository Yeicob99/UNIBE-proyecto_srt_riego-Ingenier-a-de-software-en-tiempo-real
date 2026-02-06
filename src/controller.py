
from dataclasses import dataclass
from typing import Optional
from .config import Thresholds

@dataclass
class ControlDecision:
    action: Optional[str]
    reason: str

class Controller:
    def __init__(self, th: Thresholds = Thresholds()):
        self.th = th
        self.state_on = False

    def decide(self, hum: float) -> ControlDecision:
        if hum < self.th.HUM_MIN and not self.state_on:
            self.state_on = True
            return ControlDecision(action='ON', reason=f"hum {hum:.2f} < min {self.th.HUM_MIN}")
        elif hum > self.th.HUM_MAX and self.state_on:
            self.state_on = False
            return ControlDecision(action='OFF', reason=f"hum {hum:.2f} > max {self.th.HUM_MAX}")
        else:
            return ControlDecision(action=None, reason="within range / no change")

    def safe_off(self) -> ControlDecision:
        if self.state_on:
            self.state_on = False
            return ControlDecision(action='OFF', reason='safe mode (sensor fault)')
        return ControlDecision(action=None, reason='already safe')
