import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Navbar from '../Layout/Navbar';

function Dashboard() {
  const { user } = useAuth();

  const cryptoTools = [
    {
      id: 'rsa-keygen',
      icon: '🔑',
      title: 'RSA Key Generation',
      description: 'Generate secure RSA public/private key pairs',
      path: '/crypto?tab=rsa-keygen',
    },
    {
      id: 'rsa-encrypt',
      icon: '🔒',
      title: 'RSA Encryption',
      description: 'Encrypt messages using RSA public key cryptography',
      path: '/crypto?tab=rsa-encrypt',
    },
    {
      id: 'rsa-decrypt',
      icon: '🔓',
      title: 'RSA Decryption',
      description: 'Decrypt ciphertext using RSA private keys',
      path: '/crypto?tab=rsa-decrypt',
    },
    {
      id: 'dh-exchange',
      icon: '🤝',
      title: 'Diffie-Hellman',
      description: 'Perform secure key exchange using DH protocol',
      path: '/crypto?tab=dh',
    },
  ];

  return (
    <div className="dashboard">
      <Navbar />
      <div className="container">
        <div className="welcome-section">
          <h1 className="welcome-title">
            Welcome back, {user?.first_name || user?.username}! 👋
          </h1>
          <p className="welcome-text">
            Choose a cryptographic tool below to get started
          </p>
        </div>

        <div className="crypto-grid">
          {cryptoTools.map((tool) => (
            <Link to={tool.path} key={tool.id} className="crypto-card">
              <div className="crypto-card-icon">{tool.icon}</div>
              <h3 className="crypto-card-title">{tool.title}</h3>
              <p className="crypto-card-desc">{tool.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
