from flask import Flask, render_template, request, redirect, url_for
#importamos la libreria mysql para la conexión
import mysql.connector
from scripts.Registrar import RegistrarDatos, AgregarDatos

#Cristo :D

app = Flask(__name__)

#Página principal (index)
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

#Página principal (index)
@app.route('/paginaAdd', methods = ['GET'])
def indexx():
    return render_template('add.html')

#formulario para registrar datos
@app.route('/registrar_datos', methods = ['GET', 'POST'])
def RegDatos():
    return RegistrarDatos()

#formulario para agregar datos
@app.route('/agregar_datos', methods = ['GET', 'POST'])
def AddDatos():
    return AgregarDatos()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
