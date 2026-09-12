from dataclasses import dataclass
from .config import settings
from .models import OrderRequest


@dataclass
class RiskState:
    emergency_stop: bool = False
    daily_pnl: float = 0.0


class RiskManager:
    def __init__(self) -> None:
        self.state = RiskState()

    def validate(self, order: OrderRequest, current_position_value: float = 0.0) -> tuple[bool, str]:
        if self.state.emergency_stop:
            return False, "Emergency stop is active"
        if self.state.daily_pnl <= -abs(settings.max_daily_loss_thb):
            return False, "Daily loss limit reached"
        order_value = order.volume * order.price
        if order_value > settings.max_order_value_thb:
            return False, f"Order value exceeds limit ({settings.max_order_value_thb:,.2f} THB)"
        if order.side == "BUY" and current_position_value + order_value > settings.max_position_value_thb:
            return False, f"Position value exceeds limit ({settings.max_position_value_thb:,.2f} THB)"
        return True, "OK"

    def set_emergency_stop(self, enabled: bool) -> None:
        self.state.emergency_stop = enabled


risk_manager = RiskManager()
