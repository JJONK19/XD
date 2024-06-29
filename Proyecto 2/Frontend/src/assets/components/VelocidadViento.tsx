import React from 'react';
import useFetch from '../hooks/UseFetch';
import styles from './styles/VelocidadViento.module.scss';

const VelocidadViento: React.FC = () => {
  const { data, loading, error } = useFetch('http://localhost:5000/api/viento');

  if (loading) return <div className={styles.loading}>Cargando...</div>;
  if (error) return <div className={styles.error}>Error: {error}</div>;

  return (
    <div className={styles.sensorData}>
      <h3>Datos de Velocidad del Viento</h3>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          {data && Object.entries(data).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VelocidadViento;
