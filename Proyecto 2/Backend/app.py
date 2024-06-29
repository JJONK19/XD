from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Para permitir peticiones desde el frontend

# Datos simulados de los sensores 
#AQUI TENDRIAN QUE IR LOS DATOS EN TIEMPO REAL DESDE LA RASPBERRY
sensor_data = {
    'temperatura': {'value': 30},
    'humedad': {'value': 60},
    'viento': {'value': 5},
    'luz': {'value': False},
    'aire': {'value': True},
    'presion': {'value': 1012}
}

# Datos simulados de estadísticas de los sensores
# AQUI EL ARCHIVO QUE GENERA ASSEMBLER PARA PODER IR COLOCANDO LAS ESTADISCTICAS
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
        'contador':3,
    },
    'viento': {
        'promedio': 5,
        'mediana': 4.8,
        'desviacionEstandar': 1,
        'maximo': 7,
        'minimo': 3,
        'moda': 5,
        'contador':4,
    },
    'luz': {
        'promedio': 300,
        'mediana': 280,
        'desviacionEstandar': 50,
        'maximo': 400,
        'minimo': 200,
        'moda': 300,
        'contador':4,
    },
    'aire': {
        'promedio': 50,
        'mediana': 48,
        'desviacionEstandar': 10,
        'maximo': 70,
        'minimo': 30,
        'moda': 50,
        'contador':7,
    },
    'presion': {
        'promedio': 1012,
        'mediana': 1011,
        'desviacionEstandar': 5,
        'maximo': 1020,
        'minimo': 1005,
        'moda': 1012,
        'contador':6,
    },
}

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
    return jsonify(sensor_stats['temperatura'])

@app.route('/api/humedad/stats', methods=['GET'])
def get_humedad_stats():
    return jsonify(sensor_stats['humedad'])

@app.route('/api/viento/stats', methods=['GET'])
def get_viento_stats():
    return jsonify(sensor_stats['viento'])

@app.route('/api/luz/stats', methods=['GET'])
def get_luz_stats():
    return jsonify(sensor_stats['luz'])

@app.route('/api/aire/stats', methods=['GET'])
def get_aire_stats():
    return jsonify(sensor_stats['aire'])

@app.route('/api/presion/stats', methods=['GET'])
def get_presion_stats():
    return jsonify(sensor_stats['presion'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
