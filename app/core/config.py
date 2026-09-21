# from functools import lru_cache

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     #Database settings
#     database_host: str = "localhost"
#     database_port: int = 5432
#     database_name: str = "postgres"
#     database_user: str = "postgres"
#     database_password: str

#     #JWI settings
#     jwt_secret_key: str
#     jwt_algorithm: str = "HS256"

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )

#     @property
#     def database_url(self) -> str:
#         return (
#             f"postgresql+psycopg://{self.database_user}:{self.database_password}"
#             f"@{self.database_host}:{self.database_port}/{self.database_name}"
#         )


# @lru_cache
# def get_settings() -> Settings:
#     return Settings()


# settings = get_settings()


from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database settings
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "EMS_DB" # Updated to match your local EMS_DB
    database_user: str = "postgres"
    database_password: str

    # JWT settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30  # Added this so it reads from .env

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        # NOTE: Use "postgresql+psycopg2" if you installed psycopg2, 
        # or keep "postgresql+psycopg" if you installed psycopg (v3)
        return (
            f"postgresql+psycopg2://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()