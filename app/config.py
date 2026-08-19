from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Intelligent Health Record & Cybersecurity Platform"
    env: str = "development"
    database_url: str = "sqlite:///./dev.db"

    # Locally-generated secret used to sign JWTs — not a third-party API key.
    # Generate your own with: python -c "import secrets; print(secrets.token_hex(32))"
    secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
