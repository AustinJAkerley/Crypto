import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function Navbar() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span>🔐</span>
        <span>CryptoLib</span>
      </div>
      <div className="navbar-nav">
        <Link to="/" className="nav-link">
          Dashboard
        </Link>
        <Link to="/crypto" className="nav-link">
          Crypto Tools
        </Link>
        <span className="nav-link" style={{ cursor: 'default' }}>
          {user?.username}
        </span>
        <button onClick={handleLogout} className="btn-logout">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
