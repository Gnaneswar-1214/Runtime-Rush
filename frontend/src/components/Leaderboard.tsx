import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import './Leaderboard.css';

interface LeaderboardEntry {
  rank: number;
  username: string;
  total_score: number;
  level1_score: number;
  level2_score: number;
  level3_score: number;
  total_time: number;
  level1_time: number;
  level2_time: number;
  level3_time: number;
  tab_switch_count: number;
}

interface LeaderboardProps {
  onClose: () => void;
}

const Leaderboard: React.FC<LeaderboardProps> = ({ onClose }) => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const data = await apiClient.getLeaderboard();
      setLeaderboard(data.leaderboard);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const getRankClass = (rank: number) => {
    if (rank === 1) return 'rank-gold';
    if (rank === 2) return 'rank-silver';
    if (rank === 3) return 'rank-bronze';
    return '';
  };

  return (
    <div className="leaderboard-overlay">
      <div className="leaderboard-container">
        <div className="leaderboard-header">
          <img src="/logo-jntu.png" alt="JNTU Logo" className="leaderboard-logo" />
          <div className="leaderboard-title-section">
            <h1 className="leaderboard-title">🏆 Leaderboard</h1>
            <p className="leaderboard-subtitle">Top performers who completed all levels</p>
          </div>
          <img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="leaderboard-logo" />
        </div>

        {loading ? (
          <div className="leaderboard-loading">
            <div className="loading-spinner"></div>
            <p>Loading leaderboard...</p>
          </div>
        ) : leaderboard.length === 0 ? (
          <div className="leaderboard-empty">
            <div className="empty-icon">📊</div>
            <h3>No Completions Yet</h3>
            <p>Be the first to complete all three levels!</p>
          </div>
        ) : (
          <div className="leaderboard-content">
            <div className="leaderboard-table-container">
              <table className="leaderboard-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Username</th>
                    <th>Total Score</th>
                    <th>Level 1</th>
                    <th>Level 2</th>
                    <th>Level 3</th>
                    <th>Total Time</th>
                    <th>Violations</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry) => (
                    <tr key={entry.rank} className={`leaderboard-row ${getRankClass(entry.rank)}`}>
                      <td className="rank-cell">
                        <span className="rank-badge">{getRankIcon(entry.rank)}</span>
                      </td>
                      <td className="username-cell">
                        <span className="username">{entry.username}</span>
                      </td>
                      <td className="score-cell total-score">
                        <span className="score-value">{entry.total_score.toFixed(2)}</span>
                        <span className="score-label">/ 300</span>
                      </td>
                      <td className="score-cell">
                        <div className="level-score">
                          <span className="score-value">{entry.level1_score.toFixed(2)}</span>
                          <span className="time-value">{formatTime(entry.level1_time)}</span>
                        </div>
                      </td>
                      <td className="score-cell">
                        <div className="level-score">
                          <span className="score-value">{entry.level2_score.toFixed(2)}</span>
                          <span className="time-value">{formatTime(entry.level2_time)}</span>
                        </div>
                      </td>
                      <td className="score-cell">
                        <div className="level-score">
                          <span className="score-value">{entry.level3_score.toFixed(2)}</span>
                          <span className="time-value">{formatTime(entry.level3_time)}</span>
                        </div>
                      </td>
                      <td className="time-cell">
                        <span className="total-time">{formatTime(entry.total_time)}</span>
                      </td>
                      <td className="violations-cell">
                        {entry.tab_switch_count > 0 ? (
                          <span className="violations-badge">
                            🚫 {entry.tab_switch_count}
                          </span>
                        ) : (
                          <span className="no-violations">✓</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        <div className="leaderboard-footer">
          <button className="close-button" onClick={onClose}>
            Close Leaderboard
          </button>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
