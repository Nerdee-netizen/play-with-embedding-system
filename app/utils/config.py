import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    ENV: str
    EMBEDDING_ENDPOINT: str
    EMBEDDING_MODEL_UID: str
    WEAVIATE_HTTP_HOST: str
    WEAVIATE_HTTP_PORT: int
    WEAVIATE_HTTP_SECURE: bool
    WEAVIATE_GRPC_HOST: str
    WEAVIATE_GRPC_PORT: int
    WEAVIATE_GRPC_SECURE: bool
    WEAVIATE_TOKEN: str = None


class LocalDevSettings(EnvSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DeployedSettings(EnvSettings):
    pass


def find_config() -> EnvSettings:
    if os.getenv("ENV") == "prod":
        return DeployedSettings()
    return LocalDevSettings()


env = find_config()
