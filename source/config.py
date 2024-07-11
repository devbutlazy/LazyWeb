from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    TELEGRAM_CHAT_ID: str
    BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file=".config.env")


settings = Settings()
