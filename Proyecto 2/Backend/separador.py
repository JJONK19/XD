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
    data = data.sort_values().astype(int).head(20) 
    with open(f'{"input"}.txt', 'w') as f:
        f.write(','.join(map(str, data.tolist())))

def separarCSV(dataBuscada):
    archivo = 'sensor_data.csv'
    try:
        df = pd.read_csv(archivo, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        df = pd.read_csv(archivo, encoding='utf-8')

    df = df.dropna(how='all', subset=df.columns[1:])
    
    if dataBuscada == 'temperatura':
        temperatura(df)
    elif dataBuscada == 'humedad':
        humedad(df)
    elif dataBuscada == 'viento':
        viento(df)
    elif dataBuscada == 'aire':
        calidadAire(df)
    elif dataBuscada == 'luz':
        clima(df)
    elif dataBuscada == 'presion':
        presion(df)
    
    
