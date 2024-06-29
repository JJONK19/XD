import React from 'react';
import useFetch from '../hooks/UseFetch';
import styles from './styles/Humedad.module.scss';

const Humedad: React.FC = () => {
  const { data: basicData, loading: basicLoading, error: basicError } = useFetch('http://localhost:5000/api/humedad');
  const { data: statsData, loading: statsLoading, error: statsError } = useFetch('http://localhost:5000/api/humedad/stats');

  if (basicLoading || statsLoading) return <div className={styles.loading}>Cargando...</div>;
  if (basicError || statsError) return <div className={styles.error}>Error: {basicError || statsError}</div>;

  return (
    <div className={styles.sensorData}>
      <h3>Datos de Humedad</h3>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          {basicData && Object.entries(basicData).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Estadísticas de Humedad</h3>
      <table className={styles.table}>
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
            <td>{statsData.promedio}</td>
            <td>{statsData.mediana}</td>
            <td>{statsData.desviacionEstandar}</td>
            <td>{statsData.maximo}</td>
            <td>{statsData.minimo}</td>
            <td>{statsData.moda}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Humedad;
