from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de la DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_NAME = os.getenv("DB_NAME", "mj_db")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") or os.getenv("DB_PASSWORD2", "")

    # CORS Config
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # JWT Config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # Cloudinary Config
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # URI de SQLAlchemy - CORREGIDO CON PUERTO Y SSL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?charset=utf8mb4&ssl_ca=&ssl_check_hostname=false"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración SSL para Aiven
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {
                'check_hostname': False
            }
        }
    }

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False
    CORS_ORIGINS = "*"

    CLOUDINARY_CLOUD_NAME = "test_cloud"
    CLOUDINARY_API_KEY = "test_key"
    CLOUDINARY_API_SECRET = "test_secret"