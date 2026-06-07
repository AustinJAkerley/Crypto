import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../Layout/Navbar';
import client from '../../api/client';

function CryptoTools() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get('tab') || 'rsa-keygen');

  // RSA Keygen state
  const [keygenBits, setKeygenBits] = useState(512);
  const [keygenResult, setKeygenResult] = useState(null);
  const [keygenLoading, setKeygenLoading] = useState(false);

  // RSA Encrypt state
  const [encryptData, setEncryptData] = useState({ m: '', N: '', e: '' });
  const [encryptResult, setEncryptResult] = useState(null);
  const [encryptLoading, setEncryptLoading] = useState(false);

  // RSA Decrypt state
  const [decryptData, setDecryptData] = useState({ c: '', p: '', q: '', e: '' });
  const [decryptResult, setDecryptResult] = useState(null);
  const [decryptLoading, setDecryptLoading] = useState(false);

  // DH state
  const [dhData, setDhData] = useState({ g: '2', p: '23', private_key: '6', B: '8' });
  const [dhResult, setDhResult] = useState(null);
  const [dhLoading, setDhLoading] = useState(false);

  const [error, setError] = useState('');

  useEffect(() => {
    const tab = searchParams.get('tab');
    if (tab) {
      setActiveTab(tab);
    }
  }, [searchParams]);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setSearchParams({ tab });
    setError('');
  };

  const handleRSAKeygen = async (e) => {
    e.preventDefault();
    setError('');
    setKeygenLoading(true);
    setKeygenResult(null);

    try {
      const response = await client.post('/crypto/rsa/keygen/', {
        num_bits: parseInt(keygenBits),
      });
      setKeygenResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate RSA keys');
    } finally {
      setKeygenLoading(false);
    }
  };

  const handleRSAEncrypt = async (e) => {
    e.preventDefault();
    setError('');
    setEncryptLoading(true);
    setEncryptResult(null);

    try {
      const response = await client.post('/crypto/rsa/encrypt/', {
        m: parseInt(encryptData.m),
        N: parseInt(encryptData.N),
        e: parseInt(encryptData.e),
      });
      setEncryptResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to encrypt message');
    } finally {
      setEncryptLoading(false);
    }
  };

  const handleRSADecrypt = async (e) => {
    e.preventDefault();
    setError('');
    setDecryptLoading(true);
    setDecryptResult(null);

    try {
      const response = await client.post('/crypto/rsa/decrypt/', {
        c: parseInt(decryptData.c),
        p: parseInt(decryptData.p),
        q: parseInt(decryptData.q),
        e: parseInt(decryptData.e),
      });
      setDecryptResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to decrypt ciphertext');
    } finally {
      setDecryptLoading(false);
    }
  };

  const handleDHExchange = async (e) => {
    e.preventDefault();
    setError('');
    setDhLoading(true);
    setDhResult(null);

    try {
      const response = await client.post('/crypto/dh/exchange/', {
        g: parseInt(dhData.g),
        p: parseInt(dhData.p),
        private_key: parseInt(dhData.private_key),
        B: parseInt(dhData.B),
      });
      setDhResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to perform DH exchange');
    } finally {
      setDhLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="dashboard">
      <Navbar />
      <div className="container">
        <div className="crypto-tools">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'rsa-keygen' ? 'active' : ''}`}
              onClick={() => handleTabChange('rsa-keygen')}
            >
              RSA Keygen
            </button>
            <button
              className={`tab ${activeTab === 'rsa-encrypt' ? 'active' : ''}`}
              onClick={() => handleTabChange('rsa-encrypt')}
            >
              RSA Encrypt
            </button>
            <button
              className={`tab ${activeTab === 'rsa-decrypt' ? 'active' : ''}`}
              onClick={() => handleTabChange('rsa-decrypt')}
            >
              RSA Decrypt
            </button>
            <button
              className={`tab ${activeTab === 'dh' ? 'active' : ''}`}
              onClick={() => handleTabChange('dh')}
            >
              Diffie-Hellman
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="tab-content">
            {/* RSA Keygen Tab */}
            {activeTab === 'rsa-keygen' && (
              <div>
                <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                  Generate RSA Key Pair
                </h2>
                <form onSubmit={handleRSAKeygen}>
                  <div className="form-group">
                    <label className="form-label">Number of Bits</label>
                    <input
                      type="number"
                      className="form-input"
                      value={keygenBits}
                      onChange={(e) => setKeygenBits(e.target.value)}
                      min="8"
                      max="2048"
                      required
                    />
                    <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
                      Recommended: 512 for demo, 2048+ for production
                    </p>
                  </div>
                  <button type="submit" className="btn-primary" disabled={keygenLoading}>
                    {keygenLoading ? 'Generating...' : 'Generate Keys'}
                  </button>
                </form>

                {keygenResult && (
                  <div className="result-box">
                    <h3 className="result-title">Generated Keys</h3>
                    <div className="result-item">
                      <span className="result-label">Prime p:</span>
                      <span className="result-value">{keygenResult.p}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Prime q:</span>
                      <span className="result-value">{keygenResult.q}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Public exponent e:</span>
                      <span className="result-value">{keygenResult.e}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Modulus N:</span>
                      <span className="result-value">{keygenResult.N}</span>
                    </div>
                    <div style={{ marginTop: '1rem', padding: '1rem', background: '#fff', borderRadius: '6px' }}>
                      <p style={{ fontWeight: '600', marginBottom: '0.5rem' }}>Public Key (N, e):</p>
                      <p style={{ fontFamily: 'monospace', fontSize: '0.875rem' }}>
                        ({keygenResult.N}, {keygenResult.e})
                      </p>
                      <button
                        type="button"
                        className="btn-secondary"
                        style={{ marginTop: '0.5rem', width: 'auto', padding: '6px 14px', fontSize: '0.8rem' }}
                        onClick={() => copyToClipboard(`N=${keygenResult.N}, e=${keygenResult.e}`)}
                      >
                        📋 Copy Public Key
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* RSA Encrypt Tab */}
            {activeTab === 'rsa-encrypt' && (
              <div>
                <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                  RSA Encryption
                </h2>
                <form onSubmit={handleRSAEncrypt}>
                  <div className="form-group">
                    <label className="form-label">Message (m)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter message as integer"
                      value={encryptData.m}
                      onChange={(e) => setEncryptData({ ...encryptData, m: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Modulus (N)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter N from public key"
                      value={encryptData.N}
                      onChange={(e) => setEncryptData({ ...encryptData, N: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Public Exponent (e)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter e from public key"
                      value={encryptData.e}
                      onChange={(e) => setEncryptData({ ...encryptData, e: e.target.value })}
                      required
                    />
                  </div>
                  <button type="submit" className="btn-primary" disabled={encryptLoading}>
                    {encryptLoading ? 'Encrypting...' : 'Encrypt'}
                  </button>
                </form>

                {encryptResult && (
                  <div className="result-box">
                    <h3 className="result-title">Encryption Result</h3>
                    <div className="result-item">
                      <span className="result-label">Original Message:</span>
                      <span className="result-value">{encryptResult.message}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Ciphertext:</span>
                      <span className="result-value">{encryptResult.ciphertext}</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* RSA Decrypt Tab */}
            {activeTab === 'rsa-decrypt' && (
              <div>
                <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                  RSA Decryption
                </h2>
                <form onSubmit={handleRSADecrypt}>
                  <div className="form-group">
                    <label className="form-label">Ciphertext (c)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter ciphertext"
                      value={decryptData.c}
                      onChange={(e) => setDecryptData({ ...decryptData, c: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Prime p</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter prime p"
                      value={decryptData.p}
                      onChange={(e) => setDecryptData({ ...decryptData, p: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Prime q</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter prime q"
                      value={decryptData.q}
                      onChange={(e) => setDecryptData({ ...decryptData, q: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Public Exponent (e)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter e"
                      value={decryptData.e}
                      onChange={(e) => setDecryptData({ ...decryptData, e: e.target.value })}
                      required
                    />
                  </div>
                  <button type="submit" className="btn-primary" disabled={decryptLoading}>
                    {decryptLoading ? 'Decrypting...' : 'Decrypt'}
                  </button>
                </form>

                {decryptResult && (
                  <div className="result-box">
                    <h3 className="result-title">Decryption Result</h3>
                    <div className="result-item">
                      <span className="result-label">Plaintext:</span>
                      <span className="result-value">{decryptResult.plaintext}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Private Exponent d:</span>
                      <span className="result-value">{decryptResult.d}</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Diffie-Hellman Tab */}
            {activeTab === 'dh' && (
              <div>
                <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>
                  Diffie-Hellman Key Exchange
                </h2>
                <form onSubmit={handleDHExchange}>
                  <div className="form-group">
                    <label className="form-label">Generator (g)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter generator"
                      value={dhData.g}
                      onChange={(e) => setDhData({ ...dhData, g: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Prime Modulus (p)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter prime modulus"
                      value={dhData.p}
                      onChange={(e) => setDhData({ ...dhData, p: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Your Private Key (a)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter your private key"
                      value={dhData.private_key}
                      onChange={(e) => setDhData({ ...dhData, private_key: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Other Party's Public Key (B)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter B = g^b mod p"
                      value={dhData.B}
                      onChange={(e) => setDhData({ ...dhData, B: e.target.value })}
                      required
                    />
                  </div>
                  <button type="submit" className="btn-primary" disabled={dhLoading}>
                    {dhLoading ? 'Computing...' : 'Compute Shared Key'}
                  </button>
                </form>

                {dhResult && (
                  <div className="result-box">
                    <h3 className="result-title">Key Exchange Result</h3>
                    <div className="result-item">
                      <span className="result-label">Your Public Key (A):</span>
                      <span className="result-value">{dhResult.your_public_key}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Their Public Key (B):</span>
                      <span className="result-value">{dhResult.their_public_key}</span>
                    </div>
                    <div className="result-item">
                      <span className="result-label">Shared Secret Key:</span>
                      <span className="result-value" style={{ fontWeight: '700', color: '#7c3aed' }}>
                        {dhResult.shared_key}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default CryptoTools;
