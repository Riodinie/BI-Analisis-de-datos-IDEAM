from flask import Flask, render_template, request
from numpy import mean
from numpy import median
from numpy import std
from statistics import mode
from math import e

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64#codifica las imagenes en cadenas de 64(ASCII)
import math
import os #para el guardado de las imagenes

app = Flask("prediccion")

@app.route("/")
def formulario_precipi():
    return render_template('index.html')
@app.route('/informacion')
def informacion():
    return render_template('informacion.html')
@app.route('/graficas')
def graficas():
    return render_template('graficas.html')
@app.route('/prediccion')
def prediccion():
    return render_template('predecir.html')
@app.route("/prediccion_precipitacion", methods=["GET","POST"])
def prediccion_precipitacion():
    # Cargar el archivo Excel en un DataFrame
    data = pd.read_excel('promedios2.xlsx', sheet_name='Precipitación')
    # Ruta del archivo CSV de salida
    csv_file = "PromClimat.csv"

    # Guardar los datos en un archivo CSV
    data.to_csv(csv_file, index=False)
    data.head(8)
    # Muestra los departamentos sin repetirlos en la columna "DEPARTAMENTO"
    departamentos_unicos = data['DEPARTAMENTO'].unique()
    print("\nDepartamentos:")
    for departamento in departamentos_unicos:
        print(departamento)

    # Solicita al usuario que ingrese el nombre del departamento a filtrar
    departamento_seleccionado = request.form.get("departamento")

    #Busca en las columnas el departamento seleccionado
    resultadoDepart = data.loc[data['DEPARTAMENTO'] == departamento_seleccionado]
    print(resultadoDepart)
    #Crea una lista de las columnas seleccionadas 
    lista_de_columnas = resultadoDepart.columns[3:15]
    print(lista_de_columnas)
    promedio = resultadoDepart[lista_de_columnas].mean() #Se saca la media de los datos dentro de esas columnas
    promediordenado = promedio.sort_values() #Ordena las promedios o media que se dio
    print("la media sera de: ")
    print(promediordenado)

    #saco la mediana de los datos numericos de todas las columnas
    mediana = resultadoDepart[lista_de_columnas].median()
    mediana_total = mediana.median()
    print("La mediana sera de: ", mediana_total)

    #Saco la desviación estandar general de todas las demas desviaciones
    desviacion = resultadoDepart[lista_de_columnas].std()
    desviacion_total = desviacion.std()
    print("La desviación estandar sera de: ", desviacion_total)
    #creo un arreglo con los meses 
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # Grafica
    fig, ax = plt.subplots(figsize=(10, 5))  # dimensiones
    ax.plot(meses, promediordenado, marker='o', linestyle='-', color='blue')
    ax.grid(True)
    ax.set_title("Distribución meses y precipitación")
    ax.set_xlabel('Meses')
    ax.set_ylabel('Precipitacion')
    img2 = BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    imagen_grafica = base64.b64encode(img2.read()).decode()

    img2_path = os.path.join("graficas", "grafico2.png")
    plt.savefig(img2_path, format='png')

    modeloregre = np.polyfit(meses, promediordenado, 3)
    predecir = np.poly1d(modeloregre)
    print(modeloregre)
    print(predecir)
    
    cantpredicion = int(request.form.get("mes"))
    cantregresion = predecir(cantpredicion)
    cantregresion_anio = cantregresion * 12
    # formato de presentación 2f quiere decir 2 decimales despues
    print(f"La cantidad de precipitación(mm) para el mes {cantpredicion} sera de: {cantregresion:.2f}")

    cantpredicion = range(1,  cantpredicion + 1)
    precipitapredi = predecir(cantpredicion)
    
    
    buffer = BytesIO()#Almacena temporalmente las imagenes
    plt.figure(figsize=(10, 5))  # dimensiones
    # modelo de predicción datos anteriores
    plt.plot(meses, promediordenado, 'o-', color='red')
    plt.xlabel('Meses')
    plt.ylabel('Precipitacion')
    plt.title('Regresion y Prediccion')
    plt.grid(True)
    plt.plot(meses, predecir(meses), '--',color='green')  # modelo de regresión
    plt.plot(cantpredicion, precipitapredi, '--',color='blue')  # datos predichos
    plt.legend(['Datos', 'Regresión', 'Predicción'])  # información

    # Guarda el gráfico en un objeto BytesIO
    img1 = BytesIO()#contenedor en memoria para datos binarios
    plt.savefig(img1, format='png')#se guarda
    img1.seek(0)#para leer el archivo
    imagen_prediccion = base64.b64encode(img1.read()).decode()#la convierte a una cadena base64
    
    graficas_guardada = f"{departamento_seleccionado}_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png" #guarda la grafica en formato png con el nombre del departamento y la fecha
    img1_path = os.path.join("graficas", graficas_guardada)
    plt.savefig(img1_path, format='png')


    data2 = pd.read_excel('diaslluvia.xlsx', sheet_name='Precipitación')
    # Ruta del archivo CSV de salida
    csv_file = "lluviaclima.csv"

    # Guardar los datos en un archivo CSV
    data2.to_csv(csv_file, index=False)
    data2.head(8)
        # Muestra los departamentos sin repetirlos en la columna "DEPARTAMENTO"
    
    departamentos_unicos = data2['DEPARTAMENTO'].unique()
    print("\nDepartamentos:")
    for departamento in departamentos_unicos:
        print(departamento)
    
    # Solicita al usuario que ingrese el nombre del departamento a filtrar
    departamento_seleccionado_lluvia = request.form.get("departamento")

    # Busca en las columnas el departamento seleccionado
    resultadoDepart = data2.loc[data2['DEPARTAMENTO']== departamento_seleccionado_lluvia]
    print(resultadoDepart)
    # Crea una lista de las columnas seleccionadas
    lista_de_columnas_lluvia = resultadoDepart.columns[3:15]
    print(lista_de_columnas_lluvia)
    # Se saca la media de los datos dentro de esas columnas
    promedio = resultadoDepart[lista_de_columnas_lluvia].mean()
    # Ordena las promedios o media que se dio
    promediordenado_lluvia = promedio.sort_values()
    print("la media sera de: ")
    print(promediordenado_lluvia)
    mediana = resultadoDepart[lista_de_columnas_lluvia].median()
    mediana_total_lluvia = mediana.median()
    print("La mediana sera de: ", mediana_total_lluvia)
    #Saco la desviación estandar general de todas las demas desviaciones
    desviacion = resultadoDepart[lista_de_columnas_lluvia].std()
    desviacion_total_lluvia = desviacion.std()
    print("La desviación estandar sera de: ", desviacion_total_lluvia)
    #creo un arreglo con los meses 
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # Grafica
    buffer = BytesIO()
    fig, ax = plt.subplots(figsize=(10, 5))  # dimensiones
    ax.plot(meses, promediordenado_lluvia, marker='o', linestyle='-', color='blue')
    ax.grid(True)
    ax.set_title("Distribución meses y dias lluvia")
    ax.set_xlabel('Meses')
    ax.set_ylabel('lluvia')

    img3 = BytesIO()#contenedor en memoria para datos binarios
    plt.savefig(img3, format='png')#se guarda
    img3.seek(0)#para leer el archivo
    lluvia_grafica = base64.b64encode(img3.read()).decode()#la convierte a una cadena base64
    modeloregre = np.polyfit(meses, promediordenado_lluvia, 3)
    predecir = np.poly1d(modeloregre)
    print(modeloregre)
    print(predecir)
    cantpredicion = int(request.form.get("mes"))
    print(cantpredicion)
    cantregresion_lluvia = int(predecir(cantpredicion))
    cantregresion_lluvia = int(cantregresion_lluvia)
    cantregresion_anio_lluvia = int(cantregresion_lluvia) * 12
    # formato de presentación 2f quiere decir 2 decimales despues
    print(f"La cantidad de precipitación(mm) para el mes {cantpredicion} sera de: {cantregresion_lluvia:.2f}")
    # Modelo Prediccion
    cantpredicion = range(1,  cantpredicion + 1)
    precipitapredi = predecir(cantpredicion)
    buffer = BytesIO()  # Almacena temporalmente las imagenes
    plt.figure(figsize=(10, 5))  # dimensiones
    # modelo de predicción datos anteriores
    plt.plot(meses, promediordenado_lluvia, 'o-', color='red')
    plt.xlabel('Meses')
    plt.ylabel('lluvia')
    plt.title('Regresion y Prediccion')
    plt.grid(True)
    plt.plot(meses, predecir(meses), '--',color='green')  # modelo de regresión
    plt.plot(cantpredicion, precipitapredi, '--',color='blue')  # datos predichos
    plt.legend(['Datos', 'Regresión', 'Predicción'])  # información
    # Guarda el gráfico en un objeto BytesIO
    img4 = BytesIO()  # contenedor en memoria para datos binarios
    plt.savefig(img4, format='png')  # se guarda
    img4.seek(0)  # para leer el archivo
    lluvia_prediccion = base64.b64encode(img4.read()).decode()

    #Renderiza la plantilla y toma los datos 
    return render_template('predecir.html', cantregresion=cantregresion, img1=imagen_prediccion, 
                           img2=imagen_grafica, promedio=promedio, promediordenado=promediordenado, 
                           lista_de_columnas=lista_de_columnas, mediana_total=mediana_total, desviacion_total=desviacion_total, 
                           departamento_seleccionado=departamento_seleccionado,img3=lluvia_grafica, img4=lluvia_prediccion, 
                           departamento=departamento_seleccionado_lluvia, 
                           cantregresion_lluvia=cantregresion_lluvia, lista_de_columnas_lluvia=lista_de_columnas_lluvia, promediordenado_lluvia=promediordenado_lluvia,
                           mediana_total_lluvia=mediana_total_lluvia, desviacion_total_lluvia=desviacion_total_lluvia,cantregresion_anio=cantregresion_anio, cantregresion_anio_lluvia=cantregresion_anio_lluvia)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8000') #Determina si el script se esta ejecutando directamente o esta siendo importado como modulo