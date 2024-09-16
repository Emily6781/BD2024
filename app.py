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
