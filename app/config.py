# configuracion (desarrollo, produccion, testing)
from datetime import timedelta
import os
from dotenv import load_dotenv
# Cargar las variables de .env
load_dotenv()

"""
Módulo de configuración para la aplicación Flask.
Este módulo define clases de configuración para diferentes entornos (desarrollo, producción, testing).
Carga variables de entorno desde un archivo .env utilizando dotenv.
Clases:
    Config:
        Configuración base para la aplicación.
        - Configuración de la base de datos (MySQL por defecto).
        - Configuración de CORS (orígenes permitidos, soporte de credenciales).
        - Configuración de JWT (clave secreta, expiración de tokens, ubicación, blacklist).
        - URI para SQLAlchemy.
        - Configuraciones generales de Flask (entorno, debug).
    TestingConfig(Config):
        Configuración específica para pruebas.
        - Usa una base de datos SQLite en memoria.
        - Activa el modo testing.
        - Desactiva debug.
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
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")
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
