# Codex task: wire Settrade Sandbox safely

You are modifying an existing FastAPI repo. Preserve the safety architecture.

Goal: implement the currently supported official Settrade Open API Python SDK in `app/adapters/settrade.py` for SANDBOX first.

Requirements:
1. Use only the current official Settrade Open API documentation/API reference; do not guess method names.
2. Credentials come only from `app.config.settings`; never expose App Secret or PIN to the browser/logs.
3. Implement: health/auth test, equity portfolio retrieval, equity order list, LIMIT equity order placement.
4. Broker ID, App Code, account number, App ID, App Secret, PIN must remain environment-driven.
5. Keep `ALLOW_LIVE_ORDERS=false` as the hard gate for any transmitted order.
6. Add integration-test scaffolding that is skipped unless explicit sandbox credentials are present.
7. Normalize SDK responses into plain dicts / `OrderResult`.
8. Add clear exception mapping; never blindly retry an order submission after an ambiguous network error.
9. Add a client-generated idempotency key / duplicate-order guard in the application layer before production use.
10. Do not add any profit guarantee or strategy that forces a daily target.
11. Run unit tests and document exact setup steps in README.

After the Sandbox adapter works, do NOT convert it to InnovestX production credentials automatically. Keep production as a separate, explicit deployment/configuration step.
