import asyncio
import signal
from .sensors import DummySoilMoistureSensor
from .controller import Controller
from .actuator import Actuator
from .storage import Storage
from .supervisor import Supervisor
from .scheduler import Scheduler

async def amain():
    sensor = DummySoilMoistureSensor()
    ctrl = Controller()
    act = Actuator()
    store = Storage()
    sup = Supervisor()
    sched = Scheduler(sensor, ctrl, act, store, sup)

    loop = asyncio.get_running_loop()


    try:

        for sig in (getattr(signal, "SIGINT", None), getattr(signal, "SIGTERM", None)):
            if sig is not None:
                loop.add_signal_handler(sig, sched.stop)
    except (NotImplementedError, RuntimeError):
        pass

    await sched.run()

if __name__ == '__main__':
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        pass