import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    DB_NAME: str  # Database name
    TELEGRAM_CHAT_ID: str  # Telegram chat ID for both user and bot
    BOT_TOKEN: str  # Telegram bot token
    BOT_ADMIN_ID: int  # Telegram bot admin ID

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_NAME}.db"

    @property
    def SYNC_DB_URL(self) -> str:
        return f"sqlite:///./{self.DB_NAME}.db"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
    )


settings = Settings()
