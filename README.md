# mj_api
API para el manejo de la base de datos del proyecto mj, utilizando flask en python.

Esta maneja las solicitudes a la base de datos de este proyecto, haciendo uso de los metodos GET, POST, PUT Y DELETE.

# IMPORTANTE DESCARGAR DEPENDENCIAS Y LIBRERIAS USANDO EL ARCHIVO "requirements.txt" CON EL SIGUIENTE COMANDO:
pip freeze > requirements.txt

# RUTAS:

## USUARIOS:
GET:
- /usuarios
Este es un ejemplo de lo que devuelve
[
    {
        "activo": true,
        "email": "mike.correa@example.com",
        "id": 6,
        "nombre": "Miqueas",
        "rol": "cliente",
        "telefono": "+54 9 2914438"
    }
]

POST:
- /usuarios
Se pasa algo asi
{
    "nombre": "Miqueas",
    "email": "mike.correa@example.com",
    "telefono": "2914439242",
    "contrasenia": "123456789"
}
Este es un ejemplo de lo que devuelve si todo sale bien si no devolvera un error
{
    "message": "Usuario creado exitosamente"
}
