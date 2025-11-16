from flask_sqlalchemy import SQLAlchemy
"""
Este módulo inicializa la extensión SQLAlchemy para su uso con Flask.
Atributos:
    db (SQLAlchemy): Instancia de SQLAlchemy utilizada para interactuar con la base de datos.
Uso:
    Importe 'db' desde este módulo para definir modelos y realizar operaciones de base de datos en la aplicación Flask.
"""

db = SQLAlchemy()