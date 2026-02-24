import React, { useEffect, useState } from 'react';
import { apiClient, Challenge, UserResponse, UserProgress } from '../services/api';
import Leaderboard from './Leaderboard';
import './ChallengeList.css';

interface ChallengeListProps {
  onSelectChallenge: (challenge: Challenge) => void;
  user: UserResponse;
}

const ChallengeList: React.FC<ChallengeListProps> = ({ onSelectChallenge, user }) => {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState(user.current_level);
  const [userProgress, setUserProgress] = useState<UserProgress | null>(null);
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  console.log('ChallengeList rendered with user:', user);
  console.log('Selected level:', selectedLevel);

  useEffect(() => {
    loadUserProgress();
    loadChallenges();
  }, [selectedLevel]);

  const loadUserProgress = async () => {
    try {
      const progress = await apiClient.getUserProgress(user.id);
      setUserProgress(progress);
      console.log('User progress:', progress);
    } catch (err) {
      console.error('Failed to load user progress:', err);
    }
  };

  const loadChallenges = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getChallenges();
      console.log('All challenges:', data);
      // Filter challenges by selected level
      const filteredData = data.filter((c: any) => {
        console.log(`Challenge "${c.title}" has level ${c.level}, filtering for level ${selectedLevel}`);
        return c.level === selectedLevel;
      });
      console.log('Filtered challenges:', filteredData);
      setChallenges(filteredData);
      setError(null);
    } catch (err) {
      setError('Failed to load challenges. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getChallengeStatus = (challenge: Challenge): string => {
    const now = new Date();
    const start = new Date(challenge.start_time);
    const end = new Date(challenge.end_time);

    console.log(`Challenge: ${challenge.title}`);
    console.log(`Now: ${now.toISOString()}`);
    console.log(`Start: ${start.toISOString()}`);
    console.log(`End: ${end.toISOString()}`);

    if (now < start) {
      console.log('Status: upcoming');
      return 'upcoming';
    }
    if (now > end) {
      console.log('Status: ended');
      return 'ended';
    }
    console.log('Status: active');
    return 'active';
  };

  const getStatusBadge = (status: string): JSX.Element => {
    const badges = {
      active: <span className="badge badge-active">Active</span>,
      upcoming: <span className="badge badge-upcoming">Upcoming</span>,
      ended: <span className="badge badge-ended">Ended</span>,
    };
    return badges[status as keyof typeof badges] || <span className="badge">Unknown</span>;
  };

  if (loading) {
    return <div className="challenge-list loading">Loading challenges...</div>;
  }

  if (error) {
    return (
      <div className="challenge-list error">
        <p>{error}</p>
        <button onClick={loadChallenges}>Retry</button>
      </div>
    );
  }

  if (challenges.length === 0) {
    return (
      <div className="challenge-list empty">
        <p>No challenges available yet.</p>
        <p className="hint">Create a challenge using the API at http://127.0.0.1:8000/docs</p>
      </div>
    );
  }

  // Check if user completed all levels
  const allLevelsCompleted = userProgress?.level1_completed && userProgress?.level2_completed && userProgress?.level3_completed;

  if (showLeaderboard) {
    return <Leaderboard onClose={() => setShowLeaderboard(false)} />;
  }

  return (
    <div className="challenge-list">
      <div className="challenge-list-header">
        <h2>Available Challenges</h2>
        <div className="header-actions">
          <div className="level-selector">
            <button
              className={`level-btn ${selectedLevel === 1 ? 'active' : ''} ${user.current_level < 1 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(1)}
              disabled={user.current_level < 1}
            >
              Level 1 {user.current_level < 1 && '🔒'}
            </button>
            <button
              className={`level-btn ${selectedLevel === 2 ? 'active' : ''} ${user.current_level < 2 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(2)}
              disabled={user.current_level < 2}
            >
              Level 2 {user.current_level < 2 && '🔒'}
            </button>
            <button
              className={`level-btn ${selectedLevel === 3 ? 'active' : ''} ${user.current_level < 3 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(3)}
              disabled={user.current_level < 3}
            >
              Level 3 {user.current_level < 3 && '🔒'}
            </button>
          </div>
          {allLevelsCompleted && (
            <button className="leaderboard-btn" onClick={() => setShowLeaderboard(true)}>
              <span className="trophy-icon">🏆</span>
              View Leaderboard
            </button>
          )}
        </div>
      </div>

      {allLevelsCompleted && (
        <div className="thank-you-banner">
          <div className="thank-you-content">
            <div className="thank-you-icon">🎉</div>
            <h2 className="thank-you-title">Thank You for Participating!</h2>
            <p className="thank-you-message">The results will be declared soon.</p>
            <p className="thank-you-prize">You have a chance to win exciting prizes! 🎁</p>
          </div>
        </div>
      )}

      <div className="challenges-grid">
        {challenges.map((challenge) => {
          const status = getChallengeStatus(challenge);
          const isCompleted = userProgress ? (
            (challenge.level === 1 && userProgress.level1_completed) ||
            (challenge.level === 2 && userProgress.level2_completed) ||
            (challenge.level === 3 && userProgress.level3_completed)
          ) : false;
          
          return (
            <div
              key={challenge.id}
              className={`challenge-card ${status} ${isCompleted ? 'completed' : ''}`}
            >
              <div className="challenge-header">
                <h3>{challenge.title}</h3>
                {isCompleted ? (
                  <span className="badge badge-completed">Completed ✓</span>
                ) : (
                  getStatusBadge(status)
                )}
              </div>
              <p className="challenge-description">{challenge.description}</p>
              <div className="challenge-meta">
                <span className="language">{challenge.language}</span>
                <span className="fragments">{challenge.fragments?.length || 0} fragments</span>
                <span className="tests">{challenge.test_cases?.length || 0} tests</span>
              </div>
              <div className="challenge-times">
                <div>Start: {new Date(challenge.start_time).toLocaleString()}</div>
                <div>End: {new Date(challenge.end_time).toLocaleString()}</div>
              </div>
              <button 
                className="start-button"
                onClick={() => !isCompleted && onSelectChallenge(challenge)}
                disabled={isCompleted}
              >
                {isCompleted ? 'Already Completed' : 'Start Challenge →'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ChallengeList;
