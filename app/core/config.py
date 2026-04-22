from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseModel):
    provider: str = "mock"
    model_name: str = "deepseek-chat"
    base_url: str | None = "https://api.deepseek.com"
    api_key: str | None = None
    temperature: float = 0.7
    timeout: float = 30.0


class Settings(BaseSettings):
    app_name: str = "Copywriting API"
    llm_provider: str = "mock"
    llm_model_name: str = "deepseek-chat"
    llm_base_url: str | None = "https://api.deepseek.com"
    llm_api_key: str | None = None
    llm_temperature: float = 0.7
    llm_timeout: float = 30.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def llm(self) -> LLMSettings:
        return LLMSettings(
            provider=self.llm_provider,
            model_name=self.llm_model_name,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key,
            temperature=self.llm_temperature,
            timeout=self.llm_timeout,
        )


settings = Settings()
