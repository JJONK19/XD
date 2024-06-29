### UNIVERSIDAD SAN CARLOS DE GUATEMALA
### FACULTAD DE INGENIERIA
### ESCUELA DE CIENCIAS Y SISTEMAS
### CURSO: LABORATORIO ARQUITECTURA DE COMPUTADORES Y ENSAMBLADORES 1
### SECCIÓN: A

<p align="center">
  <img width="460" height="300" src="https://upload.wikimedia.org/wikipedia/commons/4/4a/Usac_logo.png">
</p>

<center><h1>Proyecto 1</h1></center>

## MANUAL TÉCNICO
<center><h3>Integrantes</h3></center>

| NOMBRE | CARNET |
|:------:|:------:|
|Daniel Alexander Barrera Figueroa|202004783|
|María José Tebalan Sanchez|202100265|
|José Estuardo Orellana Leonardo|201314455|
|Maria de los angeles Paz de Leon|201602619|
|Josué Javier Aguilar López|201909035|
|Isai dardon mayen|202200033|
|Evelio Marcos Josue Cruz Soliz |202010040|



## Gastos realizados
___
| Componente | Costo |
|:------:|:------:|
|Materiales de la maqueta|Q30|
|ADC ADSL1115 |Q75|
|Módulo para encoder óptico |Q29|
|Disco para encoder óptico |Q7.50|
|Sensor de presiónn barométrica BMP280|Q26|
|Sensor de humedad y temperatura digital de precisión|Q39|
|MQ-135|Q35|
|TOTAL|Q241.50|  

## Backend
___

### Sensores.py
Está diseñado para ser modular y manejar diferentes tipos de datos de sensores ambientales

```python
from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/api/temperatura', methods=['GET'])
def get_temperatura():
    data = {
        'description': 'Monitoreo de la temperatura ambiente en grados centígrados.',
        'valor': random.uniform(15.0, 30.0)  # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/humedad', methods=['GET'])
def get_humedad():
    data = {
        'description': 'Medición de la humedad relativa en el ambiente.',
        'valor': random.uniform(50.0, 80.0)  # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/viento', methods=['GET'])
def get_viento():
    data = {
        'description': 'Detección de la rapidez del viento con anemómetros.',
        'valor': random.uniform(0.0, 15.0)  # Simulando un valor aleatorio
    }
    return jsonify(data)

@app.route('/api/luz', methods=['GET'])
def get_luz():
    data = {
        'description': 'Medición de la cantidad de luz ambiental para determinar si está soleado o nublado.',
        'estado': random.choice(['Soleado', 'Nublado'])  # Simulando el estado
    }
    return jsonify(data)

@app.route('/api/aire', methods=['GET'])
def get_aire():
    data = {
        'description': 'Monitoreo de los niveles de partículas y gases en el aire.',
        'estado': random.choice(['Buena', 'Mala'])  # Simulando el estado
    }
    return jsonify(data)

@app.route('/api/presion', methods=['GET'])
def get_presion():
    data = {
        'description': 'Registro de la presión atmosférica para prever cambios climáticos.',
        'valor': random.uniform(980, 1050)  # Simulando un valor aleatorio
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```

**Clase IluminacionGeneral:**
Controla las luces de diferentes áreas mediante pines GPIO.
```python
class IluminacionGeneral:
    def __init__(self):
        self.encendido = {
            'reception': False,
            'conference': False,
            'workArea': False,
            'admin': False,
            'loading': False,
            'cafeteria': False,
            'bathroom': False,
            'exterior': False
        }
        self.pines = {
            'reception': PIN_LED_reception,
            'conference': PIN_LED_conference,
            'workArea': PIN_LED_workArea,
            'admin': PIN_LED_admin,
            'loading': PIN_LED_loading,
            'cafeteria': PIN_LED_cafeteria,
            'bathroom': PIN_LED_bathroom,
            'exterior': PIN_LED_exterior
        }
    
    def switch(self, clave):
        self.encendido[clave] = not self.encendido[clave]
        GPIO.output(self.pines[clave], self.encendido[clave])
        print("Se ha encendido " + str(clave))

```

### aplicacion.py
Actualiza el tiempo de carga 

### backend.py
Se carga de backend para la lectura de sensores
```python
# Function to read BMP280 pressure data
def read_bmp280_pressure():
    global bmp280_pressure
    while True:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
            bmp280.sea_level_pressure = 1013.25
            print("BMP280 initialized successfully")
            while True:
                with data_lock:
                    bmp280_pressure = bmp280.pressure
                time.sleep(2)
        except Exception as e:
            print(f"Failed to initialize BMP280: {e}. Retrying in 5 seconds...")
            time.sleep(1)
``` 

### requirements.txt
eparar el csv por archivos separados
```txt
Flask==2.0.2
Flask-CORS==3.0.10
Werkzeug==2.0.3
pandas==2.2.2
``` 

### sensors.py
Actualizar la lectura de los sensores al front

### separador.py
Actualizzar el archivo de datos para adaptarse al asm
```python
import pandas as pd
import re

def filtrarNegativos(data):
    return data[data >= 0]

def presion(df):
    columnName = 'BMP280 Pressure (hPa)'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "presion")

def temperatura(df):
    columnName = 'AHT10 Temperature (°C)'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "temperatura")

def humedad(df):
    columnName = 'AHT10 Humidity (%)'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "humedad")

def viento(df):
    columnName = 'Wind Speed (m/s)'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "viento")

def calidadAire(df):
    columnName = 'Air Quality (ppm)'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "calidadAire")

def clima(df):
    columnName = 'Cloudy/Sunny'
    columnData = df[[columnName]].dropna()[columnName]
    filteredData = filtrarNegativos(columnData)
    crearCSV(filteredData, "clima")

def crearCSV(data, columnName):
    with open(f'{"input"}.txt', 'w') as f:
        f.write(','.join(map(str, data.tolist())))

def separarCSV(dataBuscada):
    archivo = 'sensor_data.csv'
    try:
        df = pd.read_csv(archivo, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        df = pd.read_csv(archivo, encoding='utf-8')

    df = df.dropna(how='all', subset=df.columns[1:])
    
    if dataBuscada == 'presion':
        presion(df)
    elif dataBuscada == 'temperatura':
        temperatura(df)
    elif dataBuscada == 'humedad':
        humedad(df)
    elif dataBuscada == 'viento':
        viento(df)
    elif dataBuscada == 'calidadAire':
        calidadAire(df)
    elif dataBuscada == 'clima':
        clima(df)

def main():
    dataBuscada = 'calidadAire'  # Cambia esto según la data que necesites procesar
    separarCSV(dataBuscada)

if __name__ == "__main__":
    main()
``` 


## frontend
___
Se empleó React para desarrollar el frontend, lo que permitió una gestión más eficiente y dinámica de la interfaz de usuario de la aplicación. Esta elección facilitó la creación de una experiencia web interactiva y receptiva, optimizando el rendimiento y la usabilidad. React se integró con Flask, que se utilizó en el backend para manejar las operaciones del servidor y la lógica de la aplicación. Esta combinación de tecnologías permitió una comunicación fluida entre el frontend y el backend, asegurando que la aplicación funcionara de manera coherente y eficiente tanto en la gestión de datos como en la presentación visual desde la web.


## ARM
___
Se utilizó ARM para hacer todas las mediciones.

## contador_limpio.s
Se manipula archivos y realizar operaciones básicas de análisis de datos en ensamblador, demostrando la interacción entre las operaciones de bajo nivel y las funciones de bibliotecas de C para entrada/salida y conversión de datos.

## desviacion.s, estadistica.s y media_mediana.s
En estos archivos es en donde se hacen todos los calculos correspondientes.