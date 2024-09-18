from flask import Flask, render_template, request, redirect, url_for
#importamos la libreria mysql para la conexión
import mysql.connector

#Cristo :D

app = Flask(__name__)

#Conexión a la base de datos
def create_connection():
    return mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "",
        database = "reto"
    )
#Página principal (index)
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

#Tabla de Paises
@app.route('/Tpaises', methods = ['GET'])
def TPais():
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM tpaises")
    tabla = cursor.fetchall()

    cursor.close()
    conn.close()
    modo = "activoP"
    return render_template('index.html', tabla=tabla, modo=modo)

#Tabla de Estados
@app.route('/Testados', methods = ['GET'])
def TEstado():
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM testados")
    tabla = cursor.fetchall()

    cursor.close()
    conn.close()
    modo = "activoE"
    return render_template('index.html', tabla=tabla, modo=modo)

#Tabla de Ciudades
@app.route('/Tciudades', methods = ['GET'])
def TCiudad():
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM tciudades")
    tabla = cursor.fetchall()

    cursor.close()
    conn.close()
    modo = "activoC"
    return render_template('index.html', tabla=tabla, modo=modo)

#Tabla de Codigos postales
@app.route('/Tcodigosp', methods = ['GET'])
def TCodigoP():
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM tcodigosp")
    tabla = cursor.fetchall()

    cursor.close()
    conn.close()
    modo = "activoCP"
    return render_template('index.html', tabla=tabla, modo=modo)

#Tabla de Codigos postales
@app.route('/Tcolonias', methods = ['GET'])
def TColonia():
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM tcolonias")
    tabla = cursor.fetchall()

    cursor.close()
    conn.close()
    modo = "activoCO"
    return render_template('index.html', tabla=tabla, modo=modo)

#Elimina paises
@app.route('/eliminaP', methods = ['POST'])
def EliminaP():
    #identificar el pais que queremos eliminar con el ID
    ID_Pais = request.form['id']
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM tpaises WHERE id = %s", (ID_Pais,))
    connection.commit()

    cursor.close()

    return render_template('/')

@app.route('/activarEd', methods = ['GET', 'POST'])
def ActivarEd():
    ID = request.form['id']
    Tabla = request.form['tabla']
    return render_template('update.html', tablaOpc = Tabla, IdOpc=ID)
    #return redirect(url_for('/editarP', id=ID, tabla=Tabla))


@app.route('/editarP', methods = ['GET', 'POST'])
def EditarP():
    if request.method == 'POST':
        id = request.form['IdOpc']
        tabla = request.form['tablaOpc']
        nuevo_nom = request.form['Nuevo']
        connection = create_connection()
        cursor = connection.cursor()

        if tabla == "tpaises":
            cursor.execute("UPDATE tpaises SET Nombre = %s WHERE id = %s", ( nuevo_nom, id))
            connection.commit()
            cursor.close()
            return redirect('/')

#Página principal (index)
@app.route('/paginaAdd', methods = ['GET'])
def indexx():
    return render_template('add.html')

#formulario para agragar datos
@app.route('/agragar_datos', methods = ['GET', 'POST'])
def agregarDatos():
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
        cursor.execute("INSERT INTO testados (Nombre, TPaises_Id) VALUES (%s, %s)",(estado, pais_id,))
        connection.commit()
        estado_id = cursor.lastrowid

        #ingresar ciudad
        cursor.execute("INSERT INTO tciudades (Nombre, TEstados_Id) VALUES (%s, %s)",(ciudad, estado_id,))
        connection.commit()
        ciudad_id = cursor.lastrowid

        # 4. Insertar Código Postal
        cursor.execute("INSERT INTO tcodigosp (Codigo, TCiudades_Id, TCiudades_TEstados_Id) VALUES (%s, %s, %s)", (codigo_postal, ciudad_id, estado_id,))
        connection.commit()
        codigo_postal_id = cursor.lastrowid

         # 5. Insertar Colonia
        cursor.execute("INSERT INTO tcolonias (Nombre,IdCiudad,	TCiudades_Id, TCiudades_TEstados_Id, TCodigosP_Id, TCodigosP_TCiudades_Id,	TCodigosP_TCiudades_TEstados_Id	) VALUES (%s, %s, %s, %s, %s, %s, %s)", (colonia, ciudad_id, ciudad_id, estado_id, codigo_postal_id, ciudad_id, estado_id))
                                            #Nombre	IdCiudad	CodigoPostal	TCiudades_Id	TCiudades_TEstados_Id	TCodigosP_Id	TCodigosP_TCiudades_Id	TCodigosP_TCiudades_TEstados_Id
        connection.commit()
        connection.close()

        return redirect('/')
        return template('add_data')

if __name__ == '__main__':
    app.run()
