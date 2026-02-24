import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Default App")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL= os.getenv("DATABASE_URL")

settings = Settings()