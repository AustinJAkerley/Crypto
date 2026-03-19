import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    const result = await register(formData);

    if (result.success) {
      navigate('/');
    } else {
      setErrors(result.error);
    }
    setLoading(false);
  };

  const getErrorMessage = (field) => {
    if (typeof errors === 'object' && errors[field]) {
      return Array.isArray(errors[field]) ? errors[field][0] : errors[field];
    }
    return null;
  };

  return (
    <div className="auth-container">
      <div className="auth-left">
        <div className="auth-logo">🔐</div>
        <div className="auth-brand">CryptoLib</div>
        <div className="auth-tagline">
          Advanced cryptographic tools and algorithms at your fingertips
        </div>
      </div>
      <div className="auth-right">
        <div className="auth-form-container">
          <h1 className="auth-title">Create account</h1>
          <p className="auth-subtitle">Get started with CryptoLib today</p>

          {typeof errors === 'string' && (
            <div className="error-message">{errors}</div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="username">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                className="form-input"
                placeholder="Choose a username"
                value={formData.username}
                onChange={handleChange}
                required
              />
              {getErrorMessage('username') && (
                <div className="error-message" style={{ marginTop: '0.5rem' }}>
                  {getErrorMessage('username')}
                </div>
              )}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                className="form-input"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              {getErrorMessage('email') && (
                <div className="error-message" style={{ marginTop: '0.5rem' }}>
                  {getErrorMessage('email')}
                </div>
              )}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="first_name">
                First Name
              </label>
              <input
                id="first_name"
                name="first_name"
                type="text"
                className="form-input"
                placeholder="Enter your first name"
                value={formData.first_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="last_name">
                Last Name
              </label>
              <input
                id="last_name"
                name="last_name"
                type="text"
                className="form-input"
                placeholder="Enter your last name"
                value={formData.last_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                className="form-input"
                placeholder="Create a password"
                value={formData.password}
                onChange={handleChange}
                required
              />
              {getErrorMessage('password') && (
                <div className="error-message" style={{ marginTop: '0.5rem' }}>
                  {getErrorMessage('password')}
                </div>
              )}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="password_confirm">
                Confirm Password
              </label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                className="form-input"
                placeholder="Confirm your password"
                value={formData.password_confirm}
                onChange={handleChange}
                required
              />
              {getErrorMessage('password_confirm') && (
                <div className="error-message" style={{ marginTop: '0.5rem' }}>
                  {getErrorMessage('password_confirm')}
                </div>
              )}
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating account...' : 'Sign up'}
            </button>
          </form>

          <div className="auth-link">
            Already have an account? <Link to="/login">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
