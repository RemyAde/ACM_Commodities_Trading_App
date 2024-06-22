import os
from dotenv import load_dotenv

load_dotenv()


class Settings():
    PROJECT_NAME: str = "ACM Commodities Trading App"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("secret_key")
    ALGORITM: str = os.getenv("algorithm")
    EMAIL: str = os.getenv("email")
    EMAIL_PWD: str = os.getenv("password")
    # ORIGINS: list = os.getenv("origins", "").split(',')

settings = Settings()