# configuracion (desarrollo, produccion, testing)
import os
from dotenv import load_dotenv
# Cargar las variables de .env
load_dotenv()
"""
Módulo de configuración para la aplicación Flask.
Este módulo carga variables de entorno desde un archivo .env y define clases de configuración
para diferentes entornos (desarrollo, producción, testing).
Clases:
    Config:
        Configuración base para la aplicación.
        - Configura la conexión a la base de datos MySQL utilizando variables de entorno.
        - Configura los orígenes permitidos para CORS.
        - Define parámetros generales de Flask como el entorno y el modo debug.
    TestingConfig(Config):
        Configuración específica para pruebas.
        - Activa el modo de testing.
        - Utiliza una base de datos SQLite en memoria para pruebas.
        - Desactiva el modo debug.
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
