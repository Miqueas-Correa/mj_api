# configuracion (desarrollo, produccion, testing)
import os
from dotenv import load_dotenv

# Cargar las variables de .env
load_dotenv()

class Config:
    # Configuración de la DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "mj_db")

    # URI de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Otras configuraciones de Flask
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"