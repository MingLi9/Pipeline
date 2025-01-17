import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://username:password@localhost:5432/auth_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sarcasm')
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    )
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', False)
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'username')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'auth_db')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
