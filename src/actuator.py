
import time

class Actuator:
    def __init__(self):
        self._on = False

    @property
    def is_on(self) -> bool:
        return self._on

    def turn_on(self):
        time.sleep(0.02)
        self._on = True
        print("[ACT] Válvula/Bomba: ON")

    def turn_off(self):
        time.sleep(0.02)
        self._on = False
        print("[ACT] Válvula/Bomba: OFF")
