from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram
    tg_api_id: int
    tg_api_hash: str
    tg_session_string: str
    tg_group_id: int
    tg_bot_token: str

    # AI
    anthropic_api_key: str
    openai_api_key: str
    claude_model: str = "claude-sonnet-4-5"
    stt_model: str = "gpt-4o-mini-transcribe"

    # Notion
    notion_token: str
    notion_sessions_db_id: str
    notion_items_db_id: str

    # GitHub
    github_token: str
    github_repo: str
    github_branch: str = "main"

    # Infrastructure
    redis_url: str = "redis://redis:6379/0"
    database_url: str
    session_gap_minutes: int = 120


settings = Settings()
