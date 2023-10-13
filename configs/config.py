from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    db_port: str
    db_host: str
    db_user: str
    db_pass: str
    db_name: str
    secret_jwt_key: str
    jwt_expire_time: int
    algorithm: str

    model_config = SettingsConfigDict(env_file=".env")
