from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    secret_key: str
    allowed_origins: str = "http://localhost:3000"

    database_url: str
    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str
    celery_result_backend: str

    legifrance_client_id: str
    legifrance_client_secret: str
    legifrance_token_url: str = "https://oauth.piste.gouv.fr/api/oauth/token"
    legifrance_api_url: str = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app"

    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
