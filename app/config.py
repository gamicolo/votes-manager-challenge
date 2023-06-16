from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):

    DATABASE_URL = "sqlite:///./votes-manager.db"
    DB_LIST_LIMIT = 50

    SECRET_KEY = "78b5f6caeb24de304595a40a591953a615a6e3513e1e9721c1d6290840afc5db"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()
