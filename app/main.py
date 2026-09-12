from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.models import OrderRequest
from app.risk import risk_manager
from app.service import adapter

app = FastAPI(title="InnovestX Auto Trader V1", version="0.1.0")
STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
async def root():
    return FileResponse(STATIC / "index.html")


@app.get("/api/status")
async def status():
    health = await adapter.health()
    return {
        "mode": settings.trading_mode.upper(),
        "allow_live_orders": settings.allow_live_orders,
        "risk": {
            "emergency_stop": risk_manager.state.emergency_stop,
            "daily_pnl": risk_manager.state.daily_pnl,
            "max_daily_loss_thb": settings.max_daily_loss_thb,
        },
        "adapter": health,
    }


@app.get("/api/portfolio")
async def portfolio():
    try:
        return await adapter.portfolio()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))


@app.get("/api/orders")
async def orders():
    try:
        return await adapter.orders()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))


@app.post("/api/orders")
async def place_order(order: OrderRequest):
    current_position_value = 0.0
    try:
        p = await adapter.portfolio()
        for pos in p.get("positions", []):
            if pos.get("symbol") == order.symbol:
                current_position_value = float(pos.get("volume", 0)) * float(pos.get("avg_price", 0))
    except Exception:
        pass

    ok, reason = risk_manager.validate(order, current_position_value)
    if not ok:
        raise HTTPException(status_code=400, detail=reason)
    try:
        return await adapter.place_order(order)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))


@app.post("/api/emergency-stop/{enabled}")
async def emergency_stop(enabled: bool):
    risk_manager.set_emergency_stop(enabled)
    return {"emergency_stop": enabled}
