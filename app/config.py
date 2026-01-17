from datetime import timedelta
import os
from dotenv import load_dotenv

# Cargar las variables de .env
load_dotenv()

"""
Módulo de configuración para la aplicación Flask.
Clases:
    Config:
        Configuración base para la aplicación, incluyendo:
            - Parámetros de conexión a la base de datos (MySQL).
            - Configuración de CORS.
            - URL del backend y tamaño máximo de contenido.
            - Configuración de JWT (clave secreta, expiración de tokens, ubicación y tipo de encabezado, blacklist).
            - URI de SQLAlchemy y opciones de seguimiento.
            - Configuración de Cloudinary para almacenamiento de imágenes.
            - Configuración del entorno y modo debug.
    TestingConfig(Config):
        Configuración específica para pruebas:
            - Activa el modo de testing.
            - Utiliza una base de datos SQLite en memoria.
            - Desactiva el modo debug.
            - Permite cualquier origen en CORS.
"""

class Config:
    # Configuración de la DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_NAME = os.getenv("DB_NAME", "mj_db")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") or os.getenv("DB_PASSWORD2", "")

    # CORS Config
    # Lista separada por coma → se convierte a python list
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_SUPPORTS_CREDENTIALS = True

    # URL del backend
    # BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")
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

    # URI de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Base de datos temporal
    DEBUG = False
    CORS_ORIGINS = "*"
    
    # Cloudinary Config para testing (opcional - puedes usar valores fake)
    CLOUDINARY_CLOUD_NAME = "test_cloud"
    CLOUDINARY_API_KEY = "test_key"
    CLOUDINARY_API_SECRET = "test_secret"