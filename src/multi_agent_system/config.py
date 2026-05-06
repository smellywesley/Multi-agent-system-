"""Application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application settings."""

    env: str = Field(default="development", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    llm_provider: str = Field(default="sambanova", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gemini-1.5-pro", alias="LLM_MODEL")
    gemini_api_key: str = Field(default="replace_me", alias="GEMINI_API_KEY")
    sambanova_api_key: str = Field(default="replace_me", alias="SAMBANOVA_API_KEY")
    openai_base_url: str = Field(
        default="https://api.sambanova.ai/v1",
        alias="OPENAI_BASE_URL",
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
