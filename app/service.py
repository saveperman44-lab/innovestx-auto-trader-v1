from app.config import settings
from app.adapters.simulator import SimulatorAdapter
from app.adapters.settrade import SettradeAdapter


def build_adapter():
    if settings.trading_mode.upper() == "SETTRADE":
        return SettradeAdapter()
    return SimulatorAdapter()


adapter = build_adapter()
