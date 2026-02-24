import React, { useState, useEffect } from 'react';
import ChallengeList from './components/ChallengeList';
import DragDropChallenge from './components/DragDropChallenge';
import Login from './components/Login';
import Register from './components/Register';
import AdminDashboard from './components/AdminDashboard';
import Header from './components/Header';
import { Challenge, UserResponse, apiClient } from './services/api';
import './App.css';

type AuthView = 'login' | 'register';

function App() {
  const [selectedChallenge, setSelectedChallenge] = useState<Challenge | null>(null);
  const [user, setUser] = useState<UserResponse | null>(null);
  const [authView, setAuthView] = useState<AuthView>('login');

  // Load user from localStorage on mount
  useEffect(() => {
    const savedUser = localStorage.getItem('runtimeRushUser');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData: UserResponse) => {
    setUser(userData);
    localStorage.setItem('runtimeRushUser', JSON.stringify(userData));
  };

  const handleRegister = (userData: UserResponse) => {
    setUser(userData);
    localStorage.setItem('runtimeRushUser', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('runtimeRushUser');
    setSelectedChallenge(null);
  };

  const handleChallengeComplete = async () => {
    // Refresh user data from backend to get updated level
    if (user) {
      try {
        const updatedUser = await apiClient.login({ username: user.username, password: '' });
        // Since we can't store password, we'll fetch progress directly
        const progress = await apiClient.getUserProgress(user.id);
        const updatedUserData = {
          ...user,
          current_level: progress.current_level
        };
        setUser(updatedUserData);
        localStorage.setItem('runtimeRushUser', JSON.stringify(updatedUserData));
      } catch (error) {
        console.error('Failed to refresh user data:', error);
        // Fallback: increment level locally
        const updatedUserData = {
          ...user,
          current_level: Math.min(user.current_level + 1, 3)
        };
        setUser(updatedUserData);
        localStorage.setItem('runtimeRushUser', JSON.stringify(updatedUserData));
      }
    }
    setSelectedChallenge(null);
  };

  // If not logged in, show auth screens
  if (!user) {
    return authView === 'login' ? (
      <Login
        onLogin={handleLogin}
        onSwitchToRegister={() => setAuthView('register')}
      />
    ) : (
      <Register
        onRegister={handleRegister}
        onSwitchToLogin={() => setAuthView('login')}
      />
    );
  }

  // If admin, show admin dashboard
  if (user.role === 'admin') {
    return (
      <AdminDashboard
        user={user}
        onLogout={handleLogout}
        onAddChallenge={() => {
          alert('Challenge creation UI coming soon! Use the API at http://127.0.0.1:8000/docs');
        }}
      />
    );
  }

  // Regular user view
  return (
    <div className="App">
      {!selectedChallenge ? (
        <>
          <Header title="⚡ Runtime Rush" subtitle="Competitive Coding Challenge Platform">
            <div className="user-info">
              <span className="welcome-text">Welcome, {user.username}!</span>
              <span className="level-badge">Level {user.current_level}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </Header>
          <ChallengeList onSelectChallenge={setSelectedChallenge} user={user} />
        </>
      ) : (
        <DragDropChallenge
          challenge={selectedChallenge}
          user={user}
          onBack={() => setSelectedChallenge(null)}
          onComplete={handleChallengeComplete}
        />
      )}
    </div>
  );
}

export default App;
