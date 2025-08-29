from flask import Flask
# from modelos.usuario import inicializar_usuarios
# from controladores.rutas_usuario import usuarios_bp

app = Flask(__name__) #creamos una instancia de la clase Flask

# inicializar_usuarios()

# # registramos el blueprint
# app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(debug=True) #iniciamos la aplicación