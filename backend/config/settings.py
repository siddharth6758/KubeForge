from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_port: int
    postgres_db: str
    redis_password: str

    @property
    def postgres_url(self):
        url = URL.create(
            drivername="postgresql+psycopg2",
            username=self.postgres_user,
            password=self.postgres_password,
            host="db",
            port=self.postgres_port,
            database=self.postgres_db,
        )
        return url

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()