from app.models import OrderRequest
from app.risk import RiskManager


def test_order_value_limit():
    rm = RiskManager()
    order = OrderRequest(symbol="PTT", side="BUY", volume=10000, price=100)
    ok, _ = rm.validate(order)
    assert not ok


def test_emergency_stop():
    rm = RiskManager()
    rm.set_emergency_stop(True)
    order = OrderRequest(symbol="PTT", side="BUY", volume=100, price=30)
    ok, reason = rm.validate(order)
    assert not ok
    assert "Emergency" in reason
