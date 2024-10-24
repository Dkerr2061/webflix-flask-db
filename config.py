import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY").encode("utf-8", "ignore")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
