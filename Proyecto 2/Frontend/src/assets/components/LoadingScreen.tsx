import React, { useEffect, useState } from 'react';
import styles from './styles/LoadingScreen.module.scss';
import logo1 from '../icons/usaclogo.png';
import logo2 from '../icons/FIUSACLOGO2.jpg';


const LoadingScreen: React.FC = () => {
  const [currentImage, setCurrentImage] = useState(0);
  const images = [
    logo1,
    logo2
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prevImage) => (prevImage + 1) % images.length);
    }, 1500); // Cambia de imagen cada 2 segundos

    return () => clearInterval(interval);
  }, [images.length]);

  return (
    <div className={styles.loadingScreen}>
      <img src={images[currentImage]} alt="Loading" className={styles.logo} />
      <div className={styles.spinner}></div>
      <p className={styles.text}>PROYECTO2-ARQUI1</p>
    </div>
  );
};

export default LoadingScreen;
