"""Application configuration."""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    OPENAI_API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    OPENAI_MODEL: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    LOCAL_LLM_BASE_URL: str = Field(
        default_factory=lambda: os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:8001")
    )
    LOCAL_LLM_MODEL: str = Field(default_factory=lambda: os.getenv("LOCAL_LLM_MODEL", "ollama/qwen3-8b"))
    LOCAL_LLM_API_KEY: str = Field(default_factory=lambda: os.getenv("LOCAL_LLM_API_KEY", ""))

    REQUEST_TIMEOUT_SECONDS: int = Field(default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT_SECONDS", 10)))


settings = Settings()