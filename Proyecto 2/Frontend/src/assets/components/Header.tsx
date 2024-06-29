import React from 'react';
import { Link } from 'react-router-dom';
import styles from './styles/Header.module.scss';
import logo from '../icons/usaclogoheader.png';

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <img src={logo} alt="logo" className={styles.image} />
        <h1>Estación Meteorológica</h1>
      </div>
      <nav>
        <ul>
          <li><Link to="/">Inicio</Link></li>
          <li><Link to="/reportes">Reportes</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;

