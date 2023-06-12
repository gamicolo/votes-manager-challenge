from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):

    DATABASE_URL = "sqlite:///./votes-manager.db"
    DB_LIST_LIMIT = 50

settings = Settings()
