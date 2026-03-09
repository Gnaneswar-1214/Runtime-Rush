import React, { useState } from 'react';
import { apiClient, UserResponse } from '../services/api';
import './Auth.css';

interface RegisterProps {
  onRegister: (user: UserResponse) => void;
  onSwitchToLogin: () => void;
}

const Register: React.FC<RegisterProps> = ({ onRegister, onSwitchToLogin }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const user = await apiClient.register({ username, email, password });
      onRegister(user);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-logos">
          <img src="/logo-jntu.png" alt="JNTU Logo" className="auth-logo" />
          <img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="auth-logo" />
        </div>
        
        <h2>🎉 Join Runtime Rush</h2>
        <p className="auth-subtitle">✨ Create your account to get started</p>
        
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>👤 Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>📧 Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>🔑 Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>🔐 Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              disabled={loading}
            />
          </div>
          {error && <div className="error-message">❌ {error}</div>}
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? '⏳ Creating account...' : '🚀 Register'}
          </button>
        </form>
        <div className="switch-auth">
          Already have an account?
          <button onClick={onSwitchToLogin}>🔐 Login here</button>
        </div>
      </div>
    </div>
  );
};

export default Register;
