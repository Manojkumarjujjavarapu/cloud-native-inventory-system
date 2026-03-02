import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@inventory_postgres:5432/inventory_db"
)

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/inventory_logs"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "super-secret-key"
    )