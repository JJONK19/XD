import React from 'react';
import styles from './SensorData.module.scss';

interface SensorDataProps {
  sensor: string;
}

const SensorData: React.FC<SensorDataProps> = ({ sensor }) => {
  return (
    <div className={styles.sensorData}>
      <h3>{sensor} Data</h3>
      {/* Aquí se mostrarán los datos procesados */}
    </div>
  );
}

export default SensorData;
