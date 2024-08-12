import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "Database_URL",
        "postgresql://default:LQ58NOTRUcnA@ep-wandering-grass-a5ybbbcz-pooler.us-east-2.aws.neon.tech:5432/verceldb?sslmode=require",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
