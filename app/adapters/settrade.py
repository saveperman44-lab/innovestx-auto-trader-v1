"""Settrade Open API adapter boundary.

This file intentionally does NOT guess SDK method names. The public API surface is
isolated here so Codex (or a developer) can wire the currently supported Settrade
Python SDK from the official API Reference without changing the rest of the app.
"""
from app.config import settings
from app.models import OrderRequest, OrderResult
from .base import TradingAdapter


class SettradeAdapter(TradingAdapter):
    def __init__(self) -> None:
        required = [settings.settrade_app_id, settings.settrade_app_secret, settings.settrade_account_no]
        if not all(required):
            raise RuntimeError("Settrade credentials/account are incomplete")

    async def health(self) -> dict:
        return {
            "ok": False,
            "adapter": "SETTRADE",
            "connected": False,
            "message": "Wire the official current Settrade Python SDK in app/adapters/settrade.py before enabling live/sandbox API calls.",
        }

    async def portfolio(self) -> dict:
        raise NotImplementedError("Settrade SDK integration not wired yet")

    async def orders(self) -> list[dict]:
        raise NotImplementedError("Settrade SDK integration not wired yet")

    async def place_order(self, order: OrderRequest) -> OrderResult:
        if not settings.allow_live_orders:
            return OrderResult(
                accepted=False,
                message="Live/Sandbox API order transmission is locked. Set ALLOW_LIVE_ORDERS=true only after adapter validation.",
                mode="SETTRADE",
            )
        raise NotImplementedError("Settrade SDK integration not wired yet")
