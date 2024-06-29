from flask import Flask, jsonify
from flask_cors import CORS
from sensors import bmp280_pressure, aht10_temperature, aht10_humidity, wind_speed, cloudy_sunny, air_quality, start_sensor_threads
from separador import separarCSV
import threading
import time
import subprocess

app = Flask(__name__)
CORS(app)  # Para permitir peticiones desde el frontend

# Datos simulados de los sensores
sensor_data = {
    'temperatura': {'value': 22.5},
    'humedad': {'value': 60},
    'viento': {'value': 5},
    'luz': {'value': False},
    'aire': {'value': True},
    'presion': {'value': 1012}
}

# Datos simulados de estadísticas de los sensores
sensor_stats = {
    'temperatura': {
        'promedio': 22,
        'mediana': 21,
        'desviacionEstandar': 2.5,
        'maximo': 30,
        'minimo': 15,
        'moda': 20,
        'contador': 20,
    },
    'humedad': {
        'promedio': 60,
        'mediana': 58,
        'desviacionEstandar': 5,
        'maximo': 70,
        'minimo': 50,
        'moda': 60,
        'contador': 20,
    },
    'viento': {
        'promedio': 5,
        'mediana': 4.8,
        'desviacionEstandar': 1,
        'maximo': 7,
        'minimo': 3,
        'moda': 5,
        'contador': 20,
    },
    'luz': {
        'promedio': 300,
        'mediana': 280,
        'desviacionEstandar': 50,
        'maximo': 400,
        'minimo': 200,
        'moda': 300,
        'contador': 20,
    },
    'aire': {
        'promedio': 50,
        'mediana': 48,
        'desviacionEstandar': 10,
        'maximo': 70,
        'minimo': 30,
        'moda': 50,
        'contador': 20,
    },
    'presion': {
        'promedio': 1012,
        'mediana': 1011,
        'desviacionEstandar': 5,
        'maximo': 1020,
        'minimo': 1005,
        'moda': 1012,
        'contador': 20,
    },
}

# Actualizar la data
def actualizar_sensor_data():
    global sensor_data
    while True:
        with threading.Lock():
            sensor_data['temperatura']['value'] = aht10_temperature if aht10_temperature is not None else 0.0
            sensor_data['humedad']['value'] = aht10_humidity if aht10_humidity is not None else 0.0
            sensor_data['viento']['value'] = wind_speed if wind_speed is not None else 0.0
            sensor_data['luz']['value'] = cloudy_sunny == 1 if cloudy_sunny is not None else True  
            sensor_data['aire']['value'] = air_quality > 150 if air_quality is not None else True  
            sensor_data['presion']['value'] = bmp280_pressure if bmp280_pressure is not None else 0.0
        time.sleep(10)  

def obtener_estadisticas(dataBuscada):
    separarCSV(dataBuscada)
    result_moda = subprocess.run(['./moda'], capture_output=True, text=True)
    result_mediana = subprocess.run(['./mediana'], capture_output=True, text=True)
    result_media = subprocess.run(['./media'], capture_output=True, text=True)
    result_desviacion = subprocess.run(['./desviacion'], capture_output=True, text=True)
    result_minimo = subprocess.run(['./minimo'], capture_output=True, text=True)
    result_maximo = subprocess.run(['./maximo'], capture_output=True, text=True)


    # Capturar el código de retorno
    return_code_moda = result_moda.returncode
    return_code_mediana = result_mediana.returncode
    return_code_media = result_media.returncode
    return_code_desviacion = result_desviacion.returncode
    return_code_minimo = result_minimo.returncode
    return_code_maximo = result_maximo.returncode

    if dataBuscada in sensor_stats:
        sensor_stats[dataBuscada].update({
            'promedio': return_code_media,
            'mediana': return_code_mediana,
            'desviacionEstandar': return_code_desviacion,
            'moda': return_code_moda,
            'maximo': return_code_maximo,
            'minimo': return_code_minimo,
        })
       
# Endpoint para la raíz
@app.route('/')
def index():
    return "Bienvenido a la API de la Estación Meteorológica"

# Endpoints para datos de sensores
@app.route('/api/temperatura', methods=['GET'])
def get_temperatura():
    return jsonify(sensor_data['temperatura'])

@app.route('/api/humedad', methods=['GET'])
def get_humedad():
    return jsonify(sensor_data['humedad'])

@app.route('/api/viento', methods=['GET'])
def get_viento():
    return jsonify(sensor_data['viento'])

@app.route('/api/luz', methods=['GET'])
def get_luz():
    return jsonify(sensor_data['luz'])

@app.route('/api/aire', methods=['GET'])
def get_aire():
    return jsonify(sensor_data['aire'])

@app.route('/api/presion', methods=['GET'])
def get_presion():
    return jsonify(sensor_data['presion'])

# Endpoints para estadísticas de sensores
@app.route('/api/temperatura/stats', methods=['GET'])
def get_temperatura_stats():
    obtener_estadisticas('temperatura')
    return jsonify(sensor_stats['temperatura'])

@app.route('/api/humedad/stats', methods=['GET'])
def get_humedad_stats():
    obtener_estadisticas('humedad')
    return jsonify(sensor_stats['humedad'])

@app.route('/api/viento/stats', methods=['GET'])
def get_viento_stats():
    obtener_estadisticas('viento')
    return jsonify(sensor_stats['viento'])

@app.route('/api/luz/stats', methods=['GET'])
def get_luz_stats():
    obtener_estadisticas('luz')
    return jsonify(sensor_stats['luz'])

@app.route('/api/aire/stats', methods=['GET'])
def get_aire_stats():
    obtener_estadisticas('aire')
    return jsonify(sensor_stats['aire'])

@app.route('/api/presion/stats', methods=['GET'])
def get_presion_stats():
    obtener_estadisticas('presion')
    return jsonify(sensor_stats['presion'])

if __name__ == '__main__':
    sensor_thread = threading.Thread(target=start_sensor_threads)
    sensor_thread.start()
    app.run(debug=True, port=5000)
    data_update_thread = threading.Thread(target=actualizar_sensor_data)
    data_update_thread.start()
    
