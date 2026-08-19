from functools import lru_cache
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    environment:str="development"
    database_url:str="postgresql+psycopg://originlens:originlens@postgres/originlens"
    redis_url:str="redis://redis:6379/0"
    secret_key:str="development-only-change-me-32-bytes"
    encryption_key:str=""
    detector_backend:str="modernbert"
    model_id:str="GeorgeDrayson/modernbert-ai-detection"
    model_revision:str|None=None
    max_characters:int=Field(50000,ge=1000,le=100000)
    max_words:int=Field(10000,ge=100,le=20000)
    @model_validator(mode="after")
    def secure(self):
        if self.environment=="production":
            if self.detector_backend=="fake": raise ValueError("fake detector forbidden in production")
            if "development" in self.secret_key or len(self.secret_key)<32: raise ValueError("production secret required")
            if not self.encryption_key: raise ValueError("production encryption key required")
        return self
@lru_cache
def get_settings(): return Settings()
