from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    DB_NAME: str  # Database name
    TELEGRAM_CHAT_ID: str  # Telegram chat ID for both user and bot
    BOT_TOKEN: str  # Telegram bot token
    BOT_ADMIN_ID: int  # Telegram bot admin ID

    model_config = SettingsConfigDict(env_file="src/app/main/config/.env")


settings = Settings()
