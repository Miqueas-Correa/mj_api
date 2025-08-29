# ejecutar el import luego de instalar la librería mysql-connector-python,
# si no sale nada en la terminal esta correcto, en caso de error reiniciar vs code.
# ejecutar comando como administrador
import mysql.connector

conexion = mysql.connector.connect(
    user='root',
    password='46093693',
    host='localhost',
    database='mj_bdd',
    port=3306
)

# revisamos si la conexión fue exitosa
if conexion.is_connected():
    print("Conexión exitosa a la base de datos")