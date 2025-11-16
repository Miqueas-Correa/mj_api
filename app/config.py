# configuracion (desarrollo, produccion, testing)
import os
from dotenv import load_dotenv
"""
Módulo de configuración para la aplicación Flask.
Este módulo carga variables de entorno desde un archivo .env y define clases de configuración
para diferentes entornos (desarrollo, producción, testing).
Clases:
    Config:
        Configuración base para la aplicación, incluyendo parámetros de conexión a la base de datos
        MySQL, URI de SQLAlchemy y opciones generales de Flask.
    TestingConfig(Config):
        Configuración específica para pruebas, utilizando una base de datos SQLite en memoria
        y habilitando el modo de testing.
"""
# Cargar las variables de .env
load_dotenv()

class Config:
    # Configuración de la DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_NAME = os.getenv("DB_NAME", "mj_db")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") or os.getenv("DB_PASSWORD2", "")

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
