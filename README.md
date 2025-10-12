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

- /usuarios?activos=valor
valor puede ser = a true o false por defecto es none, esto quiere decir que dara por default la lista entera si es true solo los usuarios activos si es false lo contrario. si no es ninguno de estos devolvera un status code 400.
{
    "error": "Error en el parámetro 'activos' debe ser 'true' o 'false'"
}

- /usuarios/<nombre>
- /usuarios/<id>
busqueda de usuario por nombre o id. esto es posible porque el nombre es unico

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

- /usuarios/comprobar/<id>
- /usuarios/comprobar/<nombre>
Comprobar contraseña. ESTO NO DEVUELVE LA CONTRASEÑA, devuelve si es correcta o no.
Se pasa algo asi:
{
    "contrasenia": "123456789"
}

PUT:
- /usuarios/<id>
Adbertencia antes de usar confirmar que es el usuario pidiendo la contraseña.
Este endpoint puede modificar todos los campos del usuario, puede modificar el que desee sin necesidad de modificar todos.
Se pasa algo asi:
{
    "contrasenia": "123456789"
}

DELETE:
- /usuarios/<id>
- /usuarios/<nombre>
En este endpoint no hace falta pasar nada en el body