
from src.controller import Controller

def test_controller_thresholds():
    c = Controller()
    d1 = c.decide(0.10)
    assert d1.action == 'ON'
    d2 = c.decide(0.40)
    assert d2.action is None
    d3 = c.decide(0.95)
    assert d3.action == 'OFF'
