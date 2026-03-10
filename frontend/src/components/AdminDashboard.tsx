import React, { useState, useEffect } from 'react';
import { apiClient, UserResponse, Challenge } from '../services/api';
import './AdminDashboard.css';

interface AdminDashboardProps {
  user: UserResponse;
  onLogout: () => void;
  onAddChallenge: () => void;
}

const AdminDashboard: React.FC<AdminDashboardProps> = ({ user, onLogout, onAddChallenge }) => {
  const [activeTab, setActiveTab] = useState<'stats' | 'users' | 'challenges' | 'create'>('stats');
  const [stats, setStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [selectedLevel, setSelectedLevel] = useState(1);
  const [challenges, setChallenges] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Helper function for ordinal suffixes
  const getOrdinalSuffix = (num: number) => {
    const j = num % 10;
    const k = num % 100;
    if (j === 1 && k !== 11) return 'st';
    if (j === 2 && k !== 12) return 'nd';
    if (j === 3 && k !== 13) return 'rd';
    return 'th';
  };

  // Challenge creation form state
  const [newChallenge, setNewChallenge] = useState({
    title: '',
    description: '',
    language: 'python',
    level: 1,
    fragments: [''],
    test_cases: [{ input: '', expected_output: '', visible: true }],
    duration_minutes: 5
  });

  useEffect(() => {
    loadStats();
  }, []);

  useEffect(() => {
    if (activeTab === 'users') {
      loadUsers();
    } else if (activeTab === 'challenges') {
      loadChallenges();
    }
  }, [activeTab, selectedLevel]);

  const loadStats = async () => {
    try {
      const data = await apiClient.getAdminStats(user.id);
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getAllUsers(user.id);
      setUsers(data);
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadChallenges = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getChallengesByLevel(selectedLevel, user.id);
      setChallenges(data);
    } catch (err) {
      console.error('Failed to load challenges:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChallenge = async (challengeId: string) => {
    if (!window.confirm('Are you sure you want to delete this challenge?')) return;
    
    try {
      await apiClient.deleteChallenge(challengeId, user.id);
      loadChallenges();
      loadStats();
    } catch (err) {
      alert('Failed to delete challenge');
    }
  };

  const handleTerminateUser = async (userId: string, username: string) => {
    if (!window.confirm(`Are you sure you want to terminate user "${username}"? This action cannot be undone!`)) return;
    
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || "https://runtime-rush-production.up.railway.app"}/api/admin/users/${userId}?admin_id=${user.id}`,
        { method: "DELETE" }
      );
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to terminate user");
      }
      
      alert(`User "${username}" has been terminated successfully`);
      loadUsers();
      loadStats();
    } catch (err: any) {
      alert(err.message || 'Failed to terminate user');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChallenge = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const now = new Date();
      const endTime = new Date(now.getTime() + newChallenge.duration_minutes * 60000);

      const challengeData: any = {
        title: newChallenge.title,
        description: newChallenge.description,
        language: newChallenge.language,
        level: newChallenge.level,
        fragments: newChallenge.fragments.map((content, index) => ({
          content,
          original_order: index + 1
        })),
        correct_solution: newChallenge.fragments.join('\n'),
        test_cases: newChallenge.test_cases,
        start_time: now.toISOString(),
        end_time: endTime.toISOString(),
        created_by: user.id
      };

      await apiClient.createChallenge(challengeData);
      alert('Challenge created successfully!');
      
      // Reset form
      setNewChallenge({
        title: '',
        description: '',
        language: 'python',
        level: 1,
        fragments: [''],
        test_cases: [{ input: '', expected_output: '', visible: true }],
        duration_minutes: 5
      });
      
      // Refresh stats and challenges
      loadStats();
      if (activeTab === 'challenges') {
        loadChallenges();
      }
    } catch (err) {
      alert('Failed to create challenge: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <img src="/logo-jntu.png" alt="JNTU Logo" className="admin-logo admin-logo-left" />
        
        <div className="admin-header-content">
          <h1>⚡ Admin Dashboard</h1>
          <div className="admin-user-info">
            <span>👋 Welcome, {user.username}</span>
            <button onClick={onLogout} className="logout-btn">🚪 Logout</button>
          </div>
        </div>
        
        <img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="admin-logo admin-logo-right" />
      </header>

      <div className="admin-tabs">
        <button
          className={activeTab === 'stats' ? 'active' : ''}
          onClick={() => setActiveTab('stats')}
        >
          📊 Statistics
        </button>
        <button
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
        <button
          className={activeTab === 'challenges' ? 'active' : ''}
          onClick={() => setActiveTab('challenges')}
        >
          🎯 Challenges
        </button>
        <button
          className={activeTab === 'create' ? 'active' : ''}
          onClick={() => setActiveTab('create')}
        >
          ➕ Create Challenge
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'stats' && stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Users</h3>
              <p className="stat-number">{stats.total_users}</p>
            </div>
            <div className="stat-card">
              <h3>Total Challenges</h3>
              <p className="stat-number">{stats.total_challenges}</p>
            </div>
            <div className="stat-card">
              <h3>Level 1 Challenges</h3>
              <p className="stat-number">{stats.challenges_by_level.level1}</p>
            </div>
            <div className="stat-card">
              <h3>Level 2 Challenges</h3>
              <p className="stat-number">{stats.challenges_by_level.level2}</p>
            </div>
            <div className="stat-card">
              <h3>Level 3 Challenges</h3>
              <p className="stat-number">{stats.challenges_by_level.level3}</p>
            </div>
            <div className="stat-card">
              <h3>Users on Level 1</h3>
              <p className="stat-number">{stats.users_by_level.level1}</p>
            </div>
            <div className="stat-card">
              <h3>Users on Level 2</h3>
              <p className="stat-number">{stats.users_by_level.level2}</p>
            </div>
            <div className="stat-card">
              <h3>Users on Level 3</h3>
              <p className="stat-number">{stats.users_by_level.level3}</p>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="users-section">
            <div className="users-header">
              <h2 className="users-title">📊 User Performance Dashboard</h2>
              <div className="users-stats">
                <div className="stat-pill">
                  <span className="stat-label">Total Users:</span>
                  <span className="stat-value">{users.length}</span>
                </div>
                <div className="stat-pill">
                  <span className="stat-label">Completed All:</span>
                  <span className="stat-value">{users.filter(u => u.level1_completed && u.level2_completed && u.level3_completed).length}</span>
                </div>
              </div>
            </div>

            {loading ? (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <p>Loading users...</p>
              </div>
            ) : users.length === 0 ? (
              <div className="loading-state">
                <p>No users found</p>
              </div>
            ) : (
              <div className="users-table-wrapper">
                <table className="users-table-modern">
                  <thead>
                    <tr>
                      <th className="col-rank">RANK</th>
                      <th className="col-username">USERNAME</th>
                      <th className="col-score">TOTAL SCORE</th>
                      <th className="col-level">LEVEL 1</th>
                      <th className="col-level">LEVEL 2</th>
                      <th className="col-level">LEVEL 3</th>
                      <th className="col-time">TOTAL TIME</th>
                      <th className="col-actions">ACTIONS</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users
                      .filter(u => u.role !== 'admin')
                      .sort((a, b) => b.total_score - a.total_score)
                      .map((u, index) => {
                        const isTopThree = index < 3;
                        const rankClass = index === 0 ? 'rank-gold' : index === 1 ? 'rank-silver' : index === 2 ? 'rank-bronze' : '';
                        
                        return (
                          <tr key={u.id} className={`user-row-modern ${rankClass}`}>
                            <td className="col-rank">
                              <div className="rank-badge-modern">
                                {isTopThree ? (
                                  <span className="medal-icon-modern">
                                    {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                                  </span>
                                ) : (
                                  <span className="rank-number-modern">#{index + 1}</span>
                                )}
                              </div>
                            </td>
                            <td className="col-username">
                              <div className="username-display">
                                <strong className="username-text">{u.username}</strong>
                                <span className="email-text">{u.email}</span>
                              </div>
                            </td>
                            <td className="col-score">
                              <div className="total-score-modern">
                                <span className="score-big">{u.total_score.toFixed(2)}</span>
                                <span className="score-small">/ 300</span>
                              </div>
                            </td>
                            <td className="col-level">
                              {u.level1_completed ? (
                                <div className="level-score-modern">
                                  <span className="level-score-value">{u.level1_score.toFixed(2)}</span>
                                  <span className="level-time-value">{u.level1_time ? `${Math.floor(u.level1_time / 60)}:${(u.level1_time % 60).toString().padStart(2, '0')}` : '0:00'}</span>
                                </div>
                              ) : (
                                <span className="level-incomplete">-</span>
                              )}
                            </td>
                            <td className="col-level">
                              {u.level2_completed ? (
                                <div className="level-score-modern">
                                  <span className="level-score-value">{u.level2_score.toFixed(2)}</span>
                                  <span className="level-time-value">{u.level2_time ? `${Math.floor(u.level2_time / 60)}:${(u.level2_time % 60).toString().padStart(2, '0')}` : '0:00'}</span>
                                </div>
                              ) : (
                                <span className="level-incomplete">-</span>
                              )}
                            </td>
                            <td className="col-level">
                              {u.level3_completed ? (
                                <div className="level-score-modern">
                                  <span className="level-score-value">{u.level3_score.toFixed(2)}</span>
                                  <span className="level-time-value">{u.level3_time ? `${Math.floor(u.level3_time / 60)}:${(u.level3_time % 60).toString().padStart(2, '0')}` : '0:00'}</span>
                                </div>
                              ) : (
                                <span className="level-incomplete">-</span>
                              )}
                            </td>
                            <td className="col-time">
                              <div className="total-time-modern">
                                {(() => {
                                  const totalTime = (u.level1_time || 0) + (u.level2_time || 0) + (u.level3_time || 0);
                                  const mins = Math.floor(totalTime / 60);
                                  const secs = totalTime % 60;
                                  return `${mins}:${secs.toString().padStart(2, '0')}`;
                                })()}
                              </div>
                            </td>
                            <td className="col-actions">
                              <button
                                className="terminate-btn"
                                onClick={() => handleTerminateUser(u.id, u.username)}
                                title="Terminate User"
                              >
                                🗑️ Terminate
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === 'challenges' && (
          <div className="challenges-section">
            <div className="challenges-header">
              <div className="level-selector">
                <button
                  className={selectedLevel === 1 ? 'active' : ''}
                  onClick={() => setSelectedLevel(1)}
                >
                  Level 1
                </button>
                <button
                  className={selectedLevel === 2 ? 'active' : ''}
                  onClick={() => setSelectedLevel(2)}
                >
                  Level 2
                </button>
                <button
                  className={selectedLevel === 3 ? 'active' : ''}
                  onClick={() => setSelectedLevel(3)}
                >
                  Level 3
                </button>
              </div>
            </div>

            {loading ? (
              <p>Loading challenges...</p>
            ) : (
              <div className="challenges-grid">
                {challenges.map((challenge) => (
                  <div key={challenge.id} className="challenge-card">
                    <h3>{challenge.title}</h3>
                    <p className="challenge-language">{challenge.language}</p>
                    <p className="challenge-description">{challenge.description.substring(0, 100)}...</p>
                    <div className="challenge-meta">
                      <span>Fragments: {challenge.fragments_count}</span>
                      <span>Tests: {challenge.test_cases_count}</span>
                    </div>
                    <button
                      className="delete-btn"
                      onClick={() => handleDeleteChallenge(challenge.id)}
                    >
                      🗑️ Delete
                    </button>
                  </div>
                ))}
                {challenges.length === 0 && (
                  <p className="no-challenges">No challenges for Level {selectedLevel}</p>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'create' && (
          <div className="create-challenge-section">
            <h2>Create New Challenge</h2>
            <form className="challenge-form" onSubmit={handleCreateChallenge}>
              <div className="form-row">
                <div className="form-group">
                  <label>Title</label>
                  <input
                    type="text"
                    value={newChallenge.title}
                    onChange={(e) => setNewChallenge({...newChallenge, title: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Language</label>
                  <select
                    value={newChallenge.language}
                    onChange={(e) => setNewChallenge({...newChallenge, language: e.target.value})}
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                  </select>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Level</label>
                  <select
                    value={newChallenge.level}
                    onChange={(e) => setNewChallenge({...newChallenge, level: parseInt(e.target.value)})}
                  >
                    <option value="1">Level 1</option>
                    <option value="2">Level 2</option>
                    <option value="3">Level 3</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Duration (minutes)</label>
                  <input
                    type="number"
                    value={newChallenge.duration_minutes}
                    onChange={(e) => setNewChallenge({...newChallenge, duration_minutes: parseInt(e.target.value)})}
                    min="1"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newChallenge.description}
                  onChange={(e) => setNewChallenge({...newChallenge, description: e.target.value})}
                  rows={3}
                  required
                />
              </div>

              <div className="form-group">
                <label>Code Fragments (in correct order)</label>
                {newChallenge.fragments.map((fragment, index) => (
                  <div key={index} className="fragment-input">
                    <span className="fragment-number">{index + 1}</span>
                    <textarea
                      value={fragment}
                      onChange={(e) => {
                        const newFragments = [...newChallenge.fragments];
                        newFragments[index] = e.target.value;
                        setNewChallenge({...newChallenge, fragments: newFragments});
                      }}
                      placeholder={`Fragment ${index + 1}`}
                      rows={2}
                      required
                    />
                    {newChallenge.fragments.length > 1 && (
                      <button
                        type="button"
                        className="remove-btn"
                        onClick={() => {
                          const newFragments = newChallenge.fragments.filter((_, i) => i !== index);
                          setNewChallenge({...newChallenge, fragments: newFragments});
                        }}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  className="add-btn"
                  onClick={() => setNewChallenge({...newChallenge, fragments: [...newChallenge.fragments, '']})}
                >
                  + Add Fragment
                </button>
              </div>

              <div className="form-group">
                <label>Test Cases</label>
                {newChallenge.test_cases.map((testCase, index) => (
                  <div key={index} className="test-case-input">
                    <div className="test-case-header">
                      <span>Test Case {index + 1}</span>
                      {newChallenge.test_cases.length > 1 && (
                        <button
                          type="button"
                          className="remove-btn"
                          onClick={() => {
                            const newTestCases = newChallenge.test_cases.filter((_, i) => i !== index);
                            setNewChallenge({...newChallenge, test_cases: newTestCases});
                          }}
                        >
                          ✕
                        </button>
                      )}
                    </div>
                    <input
                      type="text"
                      placeholder="Input (leave empty if none)"
                      value={testCase.input}
                      onChange={(e) => {
                        const newTestCases = [...newChallenge.test_cases];
                        newTestCases[index].input = e.target.value;
                        setNewChallenge({...newChallenge, test_cases: newTestCases});
                      }}
                    />
                    <input
                      type="text"
                      placeholder="Expected Output"
                      value={testCase.expected_output}
                      onChange={(e) => {
                        const newTestCases = [...newChallenge.test_cases];
                        newTestCases[index].expected_output = e.target.value;
                        setNewChallenge({...newChallenge, test_cases: newTestCases});
                      }}
                      required
                    />
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={testCase.visible}
                        onChange={(e) => {
                          const newTestCases = [...newChallenge.test_cases];
                          newTestCases[index].visible = e.target.checked;
                          setNewChallenge({...newChallenge, test_cases: newTestCases});
                        }}
                      />
                      Visible to participants
                    </label>
                  </div>
                ))}
                <button
                  type="button"
                  className="add-btn"
                  onClick={() => setNewChallenge({
                    ...newChallenge,
                    test_cases: [...newChallenge.test_cases, { input: '', expected_output: '', visible: true }]
                  })}
                >
                  + Add Test Case
                </button>
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? 'Creating...' : 'Create Challenge'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
