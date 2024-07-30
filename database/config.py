from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str  # Database name
    TELEGRAM_CHAT_ID: str  # Your and bot chat ID in telegram
    BOT_TOKEN: str  # Telegram bot token

    model_config = SettingsConfigDict(env_file=".config.env")


settings = Settings()
