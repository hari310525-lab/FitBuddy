from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FitBuddy"
    APP_VERSION: str = "2.0.0"

    DATABASE_URL: str = "sqlite:///./fitbuddy.db"

    GOOGLE_API_KEY: str = ""

    GEMINI_WORKOUT_MODEL: str = "gemini-2.5-pro"
    GEMINI_TIP_MODEL: str = "gemini-2.5-flash"

    AI_MODE: str = "demo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()