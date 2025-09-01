from flask import Flask
from flask_mysqldb import MySQL #importamos la clase MySQL
from controller.usuarios_controller import usuarios_bp #importamos el blueprint de usuarios

app = Flask(__name__) #creamos una instancia de la clase Flask

# conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Miqueas1'
app.config['MYSQL_DB'] = 'proyecto_mj'

conexion = MySQL(app) #creamos una instancia de la clase MySQL

# # registramos el blueprint
app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(debug=True) #iniciamos la aplicación