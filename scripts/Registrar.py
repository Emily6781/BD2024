
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

#Conexión a la base de datos
def create_connection():
    return mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "",
        database = "reto"
    )

def RegistrarDatos():
    if request.method == 'POST':
        #Relación de variables
        pais = request.form['pais']
        estado = request.form['estado']
        ciudad = request.form['ciudad']
        codigo_postal = request.form['codigo_postal']
        colonia = request.form['colonia']
        connection = create_connection()
        cursor = connection.cursor()

        #ingresar pais
        cursor.execute("INSERT INTO tpaises (Nombre) VALUES (%s)",(pais,))
        connection.commit() #envia la decalraciòn al servidor de MySQL y confirma la transacciòn
        pais_id = cursor.lastrowid #devuelve el valor generado para el autoingramentable

        #ingresar estado
        cursor.execute("INSERT INTO testados (Nombre, TPaises_Id) VALUES (%s, %s)",(estado, pais_id))
        connection.commit()
        estado_id = cursor.lastrowid

        #ingresar ciudad
        cursor.execute("INSERT INTO tciudades (Nombre, TEstados_Id) VALUES (%s, %s)",(ciudad, estado_id))
        connection.commit()
        ciudad_id = cursor.lastrowid

        # 4. Insertar Código Postal
        cursor.execute("INSERT INTO tcodigosp (Codigo, TCiudades_Id, TCiudades_TEstados_Id) VALUES (%s, %s, %s)", (codigo_postal, ciudad_id, estado_id))
        connection.commit()
        codigo_postal_id = cursor.lastrowid

         # 5. Insertar Colonia
        cursor.execute("INSERT INTO tcolonias (Nombre,IdCiudad,	TCiudades_Id, TCiudades_TEstados_Id, TCodigosP_Id, TCodigosP_TCiudades_Id,	TCodigosP_TCiudades_TEstados_Id	) VALUES (%s, %s, %s, %s, %s, %s, %s)", (colonia, ciudad_id, ciudad_id, estado_id, codigo_postal_id, ciudad_id, estado_id))
                                            #Nombre	IdCiudad	CodigoPostal	TCiudades_Id	TCiudades_TEstados_Id	TCodigosP_Id	TCodigosP_TCiudades_Id	TCodigosP_TCiudades_TEstados_Id
        connection.commit()
        connection.close()
        return render_template('index.html')

#registrar Pais
def RegistrarPais():
    if request.method == 'POST':
        #Relación de variables
        pais = request.form['pais']
        connection = create_connection()
        cursor = connection.cursor()

        #ingresar pais
        cursor.execute("INSERT INTO tpaises (Nombre) VALUES (%s)",(pais,))
        connection.commit() #envia la decalraciòn al servidor de MySQL y confirma la transacciòn
        #pais_id = cursor.lastrowid #devuelve el valor generado para el autoingramentable
        connection.close()
        return render_template('add.html')

#registrar Estado
def RegistrarEstado():
    if request.method == 'POST':
        #Relación de variables
        pais_id = request.form['pais_Id']
        estado = request.form['estado']
        connection = create_connection()
        cursor = connection.cursor()

        #ingresar estado
        cursor.execute("INSERT INTO testados (Nombre, TPaises_Id) VALUES (%s, %s)",(estado, pais_id))

        connection.commit()
        connection.close()
        return render_template('add.html')

#registrar Ciudad
def RegistrarCiudad():
    if request.method == 'POST':
        #Relación de variables
        estado_id = request.form['estado_Id']
        ciudad_id = request.form['ciudad_Id']
        connection = create_connection()
        cursor = connection.cursor()

        #ingresar ciudad
        cursor.execute("INSERT INTO tciudades (Nombre, TEstados_Id) VALUES (%s, %s)",(ciudad_id, estado_id))

        connection.commit()
        connection.close()
        return render_template('add.html')
"""
#registrar Codigo Postal
def RegistrarCodigoPostal():
    if request.method == 'POST':
        #Relación de variables
        codigoPostal = request.form['CodigoPostal']
        ciudad_id = request.form['ciudad_Id']
        connection = create_connection()
        cursor = connection.cursor()

        # 4. Insertar Código Postal
        cursor.execute("INSERT INTO tcodigosp (Codigo, TCiudades_Id, TCiudades_TEstados_Id) VALUES (%s, %s, %s)", (codigoPostal, ciudad_id, estado_id))

        connection.commit()
        connection.close()
        return render_template('add.html') """

def AgregarDatos():
    return('add.html')

#Mostrar las peticiones encoladas
def Mlistausuarios():
    UsuariosAc = UsuariosA(RegresaUsuariosG())
    UsuariosIn = UsuariosI(RegresaUsuariosG())
    ipsb = ipsB
    # Colocamos la página principal
    return render_template('listausuarios.html', UsuariosA = UsuariosAc, UsuariosI=UsuariosIn, ipsB=ipsb)

def ObtenerPaises():
    """Recupera todos los países de la base de datos."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tpaises")
        paises = cursor.fetchall()
        return paises
        #return [pais['Nombre'] for pais in paises]
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def ObtenerEstados():
    """Recupera todos los estados de la base de datos."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM testados")
        estados = cursor.fetchall()
        return estados
        #return [estado['Nombre'] for estado in estados]
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def ObtenerCiudades():
    """Recupera todas las ciudades de la base de datos."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tciudades")
        ciudades = cursor.fetchall()
        return ciudades
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def ObtenerCodigosPostales(ciudad_id):
    """Recupera los códigos postales que pertenecen a la ciudad con el ID proporcionado."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        # Consulta SQL para obtener los códigos postales que coinciden con el id de la ciudad
        query = """
            SELECT Id, Codigo
            FROM tcodigosp
            WHERE TCiudades_Id = %s
        """
        cursor.execute(query, (ciudad_id,))
        codigos_postales = cursor.fetchall()
        return codigos_postales
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def BuscarPais(name):
    """Busca un país por nombre y devuelve su ID si se encuentra."""
    connection = create_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id FROM tpaises WHERE Nombre = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        if result:
            return result['id']
        else:
            print(f"El país '{name}' no se encuentra en la base de datos.")
            return None
    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
