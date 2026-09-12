from abc import ABC, abstractmethod
from app.models import OrderRequest, OrderResult


class TradingAdapter(ABC):
    @abstractmethod
    async def health(self) -> dict: ...

    @abstractmethod
    async def portfolio(self) -> dict: ...

    @abstractmethod
    async def orders(self) -> list[dict]: ...

    @abstractmethod
    async def place_order(self, order: OrderRequest) -> OrderResult: ...
