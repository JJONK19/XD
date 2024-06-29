import React, { useState, useEffect } from 'react';
import styles from './styles/Reports.module.scss';
import useFetch from '../hooks/UseFetch';

interface SensorStats {
  promedio: number;
  mediana: number;
  desviacionEstandar: number;
  maximo: number;
  minimo: number;
  moda: number;
  contador: number; // Añadimos el campo contador
}

const sensorEndpoints: { [key: string]: string } = {
  temperatura: 'http://localhost:5000/api/temperatura/stats',
  humedad: 'http://localhost:5000/api/humedad/stats',
  viento: 'http://localhost:5000/api/viento/stats',
  luz: 'http://localhost:5000/api/luz/stats',
  aire: 'http://localhost:5000/api/aire/stats',
  presion: 'http://localhost:5000/api/presion/stats',
};

const Reportes: React.FC = () => {
  const [selectedSensor, setSelectedSensor] = useState<string>('temperatura');
  const { data, loading, error } = useFetch<SensorStats>(sensorEndpoints[selectedSensor]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      // Lógica para actualizar la información cada 10 segundos
    }, 10000);
    return () => clearInterval(intervalId);
  }, [selectedSensor]);

  return (
    <div className={styles.reportes}>
      <h2>Reportes Meteorológicos</h2>
      <div className={styles.selector}>
        <label htmlFor="sensor-select">Seleccionar Sensor: </label>
        <select id="sensor-select" value={selectedSensor} onChange={(e) => setSelectedSensor(e.target.value)}>
          <option value="temperatura">Temperatura</option>
          <option value="humedad">Humedad</option>
          <option value="viento">Velocidad del Viento</option>
          <option value="luz">Luminosidad</option>
          <option value="aire">Calidad del Aire</option>
          <option value="presion">Presión</option>
        </select>
      </div>
      <div className={styles.sensorDataContainer}>
        {loading && <p>Cargando datos...</p>}
        {error && <p>Error: {error}</p>}
        {data && (
          <>
           
            <table className={styles.sensorTable}>
              <thead>
                <tr>
                  <th>Promedio</th>
                  <th>Mediana</th>
                  <th>Desviación Estándar</th>
                  <th>Máximo</th>
                  <th>Mínimo</th>
                  <th>Moda</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{data.promedio}</td>
                  <td>{data.mediana}</td>
                  <td>{data.desviacionEstandar}</td>
                  <td>{data.maximo}</td>
                  <td>{data.minimo}</td>
                  <td>{data.moda}</td>
                </tr>
              </tbody>
            </table>
            <div className={styles.counter}>
              <h3>Contador</h3>
              <p>{data.contador}</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Reportes;
