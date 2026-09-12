import itertools
from app.models import OrderRequest, OrderResult
from .base import TradingAdapter


class SimulatorAdapter(TradingAdapter):
    def __init__(self) -> None:
        self._ids = itertools.count(100001)
        self._orders: list[dict] = []
        self._cash = 1_000_000.0
        self._positions: dict[str, dict] = {}

    async def health(self) -> dict:
        return {"ok": True, "adapter": "SIMULATOR", "connected": True}

    async def portfolio(self) -> dict:
        return {
            "account": "SIMULATOR",
            "cash": self._cash,
            "positions": list(self._positions.values()),
        }

    async def orders(self) -> list[dict]:
        return list(reversed(self._orders))

    async def place_order(self, order: OrderRequest) -> OrderResult:
        order_id = f"SIM-{next(self._ids)}"
        value = order.volume * order.price
        if order.side == "BUY":
            if value > self._cash:
                return OrderResult(accepted=False, message="Insufficient simulator cash", mode="SIMULATOR")
            self._cash -= value
            pos = self._positions.setdefault(order.symbol, {"symbol": order.symbol, "volume": 0, "avg_price": 0.0})
            old_volume = pos["volume"]
            new_volume = old_volume + order.volume
            pos["avg_price"] = ((old_volume * pos["avg_price"]) + value) / new_volume
            pos["volume"] = new_volume
        else:
            pos = self._positions.get(order.symbol)
            if not pos or pos["volume"] < order.volume:
                return OrderResult(accepted=False, message="Insufficient simulator position", mode="SIMULATOR")
            pos["volume"] -= order.volume
            self._cash += value
            if pos["volume"] == 0:
                self._positions.pop(order.symbol, None)

        self._orders.append({
            "order_id": order_id,
            "symbol": order.symbol,
            "side": order.side,
            "volume": order.volume,
            "price": order.price,
            "status": "FILLED_SIMULATED",
        })
        return OrderResult(accepted=True, order_id=order_id, message="Simulated order filled", mode="SIMULATOR")
