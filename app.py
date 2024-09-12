from flask import Flask, render_template, request, redirect, url_for, jsonify
#importamos la libreria mysql para la conexión
import mysql.connector
from scripts.Registrar import RegistrarDatos, AgregarDatos, ObtenerPaises, ObtenerEstados, ObtenerCiudades, ObtenerCodigosPostales, RegistrarPais, RegistrarEstado, RegistrarCiudad #,RegistrarCodigoPostal

#Cristo :D

app = Flask(__name__)

#Página principal (index)
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

#Página principal (index)
@app.route('/paginaAdd', methods = ['GET'])
def indexx():
    OPaises = ObtenerPaises()
    OEstados = ObtenerEstados()
    OCiudades = ObtenerCiudades()
    return render_template('add.html', paises = OPaises, estados = OEstados, ciudades = OCiudades)

#formulario para registrar datos
@app.route('/registrar_datos', methods = ['GET', 'POST'])
def RegDatos():
    return RegistrarDatos()

#formulario para agregar datos
@app.route('/agregar_datos', methods = ['GET', 'POST'])
def AddDatos():
    return AgregarDatos()

#registrar pais
@app.route('/registrar_pais', methods = ['POST'])
def RegPais():
    RegistrarPais()
    return redirect('/paginaAdd')

#registrar estado
@app.route('/registrar_estado', methods = ['POST'])
def RegEstado():
    RegistrarEstado()
    return redirect('/paginaAdd')

#registrar ciudad
@app.route('/registrar_ciudad', methods = ['POST'])
def RegCiudad():
    RegistrarCiudad()
    return redirect('/paginaAdd')
"""
#registrar codigo postal
@app.route('/registrar_codigopostal', methods = ['POST'])
def RegCodPostal():
    RegistrarCodigoPostal()
    return redirect('/paginaAdd')
    """

@app.route('/obtener_codigos_postales')
def obtener_codigos_postales_endpoint():
    ciudad_id = request.args.get('ciudad_id')
    codigos_postales = ObtenerCodigosPostales(ciudad_id)
    return jsonify({'codigos_postales': codigos_postales})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
