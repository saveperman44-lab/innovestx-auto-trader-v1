# InnovestX Auto Trader V1

Safety-first starter web app for building an automated trading interface around Settrade Open API / InnovestX.

## Current state

- Working FastAPI web dashboard
- Working local simulator (default)
- Buy/Sell test orders in simulator
- Portfolio and order history
- Risk guardrails: max order value, max position value, daily loss limit hook
- Emergency stop
- Secrets are server-side via `.env`
- Settrade integration is isolated in `app/adapters/settrade.py`
- Real/Sandbox API transmission is intentionally locked until the official current SDK calls are wired and tested

## Run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows CMD
# cp .env.example .env  # macOS/Linux
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Sandbox credentials

Put credentials only in `.env`. Never paste `Application Secret`, production PIN, or production App Secret into frontend code or Git.

For Settrade sandbox the portal may provide values such as Broker ID `SANDBOX`, App Code `SANDBOX`, a sandbox equity account, and sandbox PIN. Use exactly the values shown in your own portal.

## Enabling Settrade mode

1. Verify the latest official Settrade Python SDK documentation.
2. Implement authentication, portfolio, order listing, and place-order methods only in `app/adapters/settrade.py`.
3. Add integration tests against Sandbox.
4. Set `TRADING_MODE=SETTRADE`.
5. Keep `ALLOW_LIVE_ORDERS=false` while testing read-only endpoints.
6. Enable order transmission only after confirming symbol, side, volume, price type, account, PIN handling, and rejection behavior in Sandbox.
7. Production InnovestX credentials must be a separate environment/configuration from Sandbox.

## Production safety gates

Do not go live until you have: idempotent order submission, duplicate-order protection, exchange session checks, price-band checks, max daily turnover, max concurrent positions, reconciliation against broker order status, persistent audit logs, credential rotation, user authentication/2FA, TLS, database backups, and a kill switch independent from the strategy engine.
