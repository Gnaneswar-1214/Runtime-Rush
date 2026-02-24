import React, { useState } from 'react';
import { apiClient, UserResponse } from '../services/api';
import './Auth.css';

interface LoginProps {
  onLogin: (user: UserResponse) => void;
  onSwitchToRegister: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin, onSwitchToRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await apiClient.login({ username, password });
      onLogin(user);
    } catch (err: any) {
      setError(err.message || 'Login failed');
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
        
        <h2>⚡ Login to Runtime Rush</h2>
        <p className="auth-subtitle">Enter your credentials to continue</p>
        
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <div className="switch-auth">
          Don't have an account?
          <button onClick={onSwitchToRegister}>Register here</button>
        </div>
      </div>
    </div>
  );
};

export default Login;
