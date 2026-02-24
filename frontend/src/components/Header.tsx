import React from 'react';
import './Header.css';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  children?: React.ReactNode;
}

const Header: React.FC<HeaderProps> = ({ title, subtitle, children }) => {
  return (
    <header className="app-header-with-logos">
      <img src="/logo-jntu.png" alt="JNTU Logo" className="header-logo header-logo-left" />
      
      <div className="header-content">
        {title && <h1>{title}</h1>}
        {subtitle && <p>{subtitle}</p>}
        {children}
      </div>
      
      <img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="header-logo header-logo-right" />
    </header>
  );
};

export default Header;
