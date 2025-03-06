import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_URL = os.getenv("API_URL")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

config = Config()
