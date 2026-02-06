
import time
from contextlib import contextmanager

@contextmanager
def deadline_timer(deadline_s: float, label: str):
    t0 = time.perf_counter()
    yield lambda: time.perf_counter() - t0
    elapsed = time.perf_counter() - t0
    if elapsed > deadline_s:
        print(f"[WARN][{label}] Deadline excedido: {elapsed*1000:.2f} ms > {deadline_s*1000:.0f} ms")
