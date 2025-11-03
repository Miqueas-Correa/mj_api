# mj_api
API para el manejo de la base de datos del proyecto mj, utilizando flask en python.

Esta maneja las solicitudes a la base de datos de este proyecto, haciendo uso de los metodos GET, POST, PUT Y DELETE.

# IMPORTANTE DESCARGAR DEPENDENCIAS Y LIBRERIAS USANDO EL ARCHIVO "requirements.txt" CON EL SIGUIENTE COMANDO:
pip freeze > requirements.txt

# RUTAS:

## USUARIOS:
El atributo activo por default siempre va a ser none en caso de no pasar el atributo valido
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
Condiciones para que funcione:

    nombre: Debe ser un str, no debe estar vacio, minimo 2 a 50 caracteres.

    email: Debe ser un str y cumplir los parametros de Google.

    telefono: Debe ser un str, y debe ser un numero verdadero argentino.

    contrasenia: Debe ser un str, no debe estar vacio, minimo 6 a 100 caracteres.

Se pasa algo asi, todos estos campos son obligatorios:
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
- /usuarios/<nombre>
Adbertencia antes de usar confirmar que es el usuario pidiendo la contraseña.
Este endpoint puede modificar todos los campos del usuario, se pueden ver en el POST, puede modificar el que desee sin necesidad de modificar todos.
Se pasa algo asi:
{
    "contrasenia": "123456789"
}

DELETE:
- /usuarios/<id>
- /usuarios/<nombre>
En este endpoint no hace falta pasar nada en el body

## PRODUCTOS:
El atributo mostrar por default siempre va a ser none en caso de no pasar el atributo valido
GET:
- /productos
ejemplo de devolucion:
[
    {
        "categoria": "Calzado",
        "descripcion": "Zapatillas para correr de alta calidad",
        "id": 1,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Zapatillas deportivas",
        "precio": 19999.99,
        "stock": 10
    }
]

GET:
- /productos?mostrar=<true o false>
Lista los productos con un filtro, esto porque se pueden ocultar los productos con el campo "mostrar".
Devolucion:
[
    {
        "categoria": "Calzado",
        "descripcion": "Zapatillas para correr de alta calidad",
        "id": 1,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Zapatillas deportivas",
        "precio": 19999.99,
        "stock": 10
    }
]

GET:
- /productos/<id>?mostrar=<true o false>
- /productos/<nombre>?mostrar=<true o false>
Este get traera todas las "concidencias" y "contiene" con el valor de "nombre" o simplemente por "id" y tambien se podra filtrar mostrar o no.
Ejemplo:
/productos/a
Devolucion:
[
    {
        "categoria": "Calzado",
        "descripcion": "Zapatillas para correr de alta calidad",
        "id": 1,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Zapatillas deportivas",
        "precio": 19999.99,
        "stock": 10
    },
    {
        "categoria": "Accesorios",
        "descripcion": "Auriculares inalámbricos con micrófono",
        "id": 3,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Auriculares Bluetooth",
        "precio": 15999.5,
        "stock": 20
    }
]

GET:
Trae una lista de todos los productos en la categoria
- /productos/categoria/<nombre de la categoria>

Ejemplo:
- /productos/categoria/electronica
Devolucion:
[
    {
        "categoria": "Electrónica",
        "descripcion": "Notebook Lenovo 15\" con Intel i5",
        "id": 2,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Notebook Lenovo",
        "precio": 350000.0,
        "stock": 5
    }
]

Tambien cuenta con "mostrar"
Ejemplo 2:
- /productos/categoria/electronica?mostrar=true
Devolucion:
[
    {
        "categoria": "Electrónica",
        "descripcion": "Notebook Lenovo 15\" con Intel i5",
        "id": 2,
        "imagen_url": "https://via.placeholder.com/200",
        "mostrar": true,
        "nombre": "Notebook Lenovo",
        "precio": 350000.0,
        "stock": 5
    }
]

POST:
En caso de que todo este correcto devolvera un status code 200
Estos son los datos que se deben pasar con sus condiciones para poder realizar la operacion:

    nombre: Debe ser un str, no puede ser none o null, debe contener almenos 2 caracteres como minimo y un maximo de 50.

    precio: Debe ser un float, no puede ser menor a 0.

    stock: Debe ser un entero, no puede ser menor a 0.

    categoria: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 100.

    descripcion: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 200.

    imagen_url: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 200.

    mostrar: Debe ser un booleano.

- /productos
Ejemplo de body:
{
    "categoria": "Electronica",
    "descripcion": "Auriculares gamers",
    "imagen_url": "https://via.placeholder.com/200",
    "mostrar": false,
    "nombre": "Ariculares A9 pro",
    "precio": 19999.99,
    "stock": 10
}

PUT:
Estos son los datos que se pueden modificar con sus condiciones para poder realizar la operacion,
todos estos atributos son opcionales se puede pasar unicamente uno o los que decee modificar:

    nombre: Debe ser un str, no puede ser none o null, debe contener almenos 2 caracteres como minimo y un maximo de 50.

    precio: Debe ser un float, no puede ser menor a 0.

    stock: Debe ser un entero, no puede ser menor a 0.

    categoria: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 100.

    descripcion: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 200.

    imagen_url: Debe ser un str, no puede ser none o null, debe contener almenos 1 caracteres como minimo y un maximo de 200.

    mostrar: Debe ser un booleano.

Se puede ralizar con id o nombre
- /productos/<id>
- /productos/<nombre>
Ejemplo de body:
{
    "precio": 19999.99,
    "stock": 10
}

## PEDIDOS:
GET: lista todo los pedidos, cuenta con un filtro para identificar los pedidos que se encuentren cerrados o no
/pedidos
/pedidos?cerrado=<true o false>
Ejemplo de devolucion:
[
    {
        "cerrado": false,
        "codigo_producto": 1,
        "fecha": "2025-09-17T19:46:26",
        "id": 1,
        "id_usuario": 2,
        "total": 19999.99
    },
    {
        "cerrado": true,
        "codigo_producto": 3,
        "fecha": "2025-09-17T19:46:26",
        "id": 2,
        "id_usuario": 3,
        "total": 15999.5
    },
    {
        "cerrado": false,
        "codigo_producto": 2,
        "fecha": "2025-09-17T19:46:26",
        "id": 3,
        "id_usuario": 2,
        "total": 350000.0
    }
]

GET:
Buscar pedido por id, cuenta con cerrado.
/pedidos/<id>
/pedidos/<id>?cerrado=<true o false>
Ejemplo de devolucion:
[
    {
        "cerrado": false,
        "codigo_producto": 2,
        "fecha": "2025-09-17T19:46:26",
        "id": 3,
        "id_usuario": 2,
        "total": 350000.0
    }
]

GET:
Obtiene los pedidos de un usuario.
/pedidos/usuario/<id>
/pedidos/usuario/<id>?cerrado=<true o false>
Ejemplo de devolucion:
[
    {
        "cerrado": false,
        "codigo_producto": 1,
        "fecha": "2025-09-17T19:46:26",
        "id": 1,
        "id_usuario": 2,
        "total": 19999.99
    },
    {
        "cerrado": false,
        "codigo_producto": 2,
        "fecha": "2025-09-17T19:46:26",
        "id": 3,
        "id_usuario": 2,
        "total": 350000.0
    }
]

GET:
Obtiene los pedidos en los que aparece un producto.
/pedidos/producto/<id>
/pedidos/producto/<id>?cerrado=<true o false>
Ejemplo de devolucion:
[
    {
        "cerrado": false,
        "codigo_producto": 2,
        "fecha": "2025-09-17T19:46:26",
        "id": 3,
        "id_usuario": 2,
        "total": 350000.0
    }
]

POST:
/pedidos
Crea los pedidos, se ingresan los siguientes datos:
    id_usuario: Debe ser un numero entero, igual o mayor a 1.
    codigo_producto: Debe ser un numero entero, igual o mayor a 1.
    total: Debe ser un numero flotante, igual o mayor a 0.

Ejemplo de body:
{
    "id_usuario": 1,
    "codigo_producto": 3,
    "total": 0
}

PUT:
/pedidos/<id>
Modifica los pedidos, los datos modificables son los siguientes, todos los datos son opcionales:
    id_usuario: Debe ser un numero entero, igual o mayor a 1.
    codigo_producto: Debe ser un numero entero, igual o mayor a 1.
    total: Debe ser un numero entero, igual o mayor a 1.
    cerrado: Debe ser true o false.

Ejemplo de body:
{
    "id_usuario": 1,
    "codigo_producto": 3,
    "total": 0,
    "cerrado": "True"
}

DELETE:
/pedidos/<int:id>
Elimina el pedido por id