import os

class Settings:
    APP_NAME = "Net-OS"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
