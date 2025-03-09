# This code defines a settings configuration class using pydantic-settings to manage environment variables in a FastAPI project.

from pydantic_settings import BaseSettings,SettingsConfigDict

# BaseSettings is a Pydantic class used to load environment variables.
# SettingsConfigDict is a configuration object that helps manage how environment variables are loaded.

class Settings(BaseSettings):
    DATABASE_URL:str
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config=Settings()