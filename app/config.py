from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    trading_mode: str = "SIMULATOR"
    settrade_app_id: str = ""
    settrade_app_secret: str = ""
    settrade_broker_id: str = "SANDBOX"
    settrade_app_code: str = "SANDBOX"
    settrade_account_no: str = ""
    settrade_pin: str = ""
    max_order_value_thb: float = 10000
    max_daily_loss_thb: float = 1000
    max_position_value_thb: float = 20000
    allow_live_orders: bool = False


settings = Settings()
