
import asyncio
import time
from collections import deque
from typing import Deque
from .config import Timing
from .utils import deadline_timer
from .sensors import SensorInterface
from .controller import Controller
from .actuator import Actuator
from .storage import Storage, Measurement, Event
from .supervisor import Supervisor

class Scheduler:
    def __init__(self, sensor: SensorInterface, ctrl: Controller, act: Actuator, store: Storage, sup: Supervisor):
        self.sensor = sensor
        self.ctrl = ctrl
        self.act = act
        self.store = store
        self.sup = sup
        self.buf: Deque[Measurement] = deque(maxlen=1000)
        self._stop = asyncio.Event()

    async def run(self):
        tasks = [
            asyncio.create_task(self._sensor_task()),
            asyncio.create_task(self._fault_task()),
            asyncio.create_task(self._storage_task()),
        ]
        await self._stop.wait()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _sensor_task(self):
        period = Timing.SENSOR_PERIOD
        while not self._stop.is_set():
            t_start = time.perf_counter()
            with deadline_timer(Timing.SENSOR_DEADLINE, 'SENSOR'):
                reading = self.sensor.read()
                ok = self.sup.validate(reading.value, reading.ts)
                self.buf.append(Measurement(ts=reading.ts, humidity=reading.value))
                if ok:
                    with deadline_timer(Timing.DECISION_DEADLINE, 'DECISION'):
                        dec = self.ctrl.decide(reading.value)
                    if dec.action == 'ON':
                        with deadline_timer(Timing.ACTUATION_DEADLINE, 'ACTUATION'):
                            self.act.turn_on()
                        self.store.insert_event(Event(ts=reading.ts, action='ON', reason=dec.reason))
                    elif dec.action == 'OFF':
                        with deadline_timer(Timing.ACTUATION_DEADLINE, 'ACTUATION'):
                            self.act.turn_off()
                        self.store.insert_event(Event(ts=reading.ts, action='OFF', reason=dec.reason))
                else:
                    dec = self.ctrl.safe_off()
                    if dec.action == 'OFF':
                        self.act.turn_off()
                        self.store.insert_event(Event(ts=reading.ts, action='OFF', reason=dec.reason))
                        print("[SAFE] Lectura inválida o ausente: riego en OFF")
            dt = time.perf_counter() - t_start
            await asyncio.sleep(max(0.0, period - dt))

    async def _fault_task(self):
        period = Timing.FAULT_PERIOD
        while not self._stop.is_set():
            t_start = time.perf_counter()
            with deadline_timer(Timing.FAULT_DEADLINE, 'FAULT-CHECK'):
                if self.sup.fault():
                    dec = self.ctrl.safe_off()
                    if dec.action == 'OFF':
                        self.act.turn_off()
                        self.store.insert_event(Event(ts=time.time(), action='OFF', reason=dec.reason))
                        print("[SAFE] Supervisor: sin datos válidos recientes → OFF")
            dt = time.perf_counter() - t_start
            await asyncio.sleep(max(0.0, period - dt))

    async def _storage_task(self):
        period = Timing.STORAGE_PERIOD
        while not self._stop.is_set():
            t_start = time.perf_counter()
            with deadline_timer(Timing.STORAGE_DEADLINE, 'STORAGE'):
                batch = list(self.buf)
                self.buf.clear()
                self.store.insert_measurements(batch)
            dt = time.perf_counter() - t_start
            await asyncio.sleep(max(0.0, period - dt))

    def stop(self):
        self._stop.set()
