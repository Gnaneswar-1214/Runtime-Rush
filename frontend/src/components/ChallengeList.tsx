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
    const loadData = async () => {
      await loadUserProgress();
      await loadChallenges();
    };
    loadData();
  }, [selectedLevel]); // eslint-disable-line react-hooks/exhaustive-deps

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
    return <div className="challenge-list loading">⏳ Loading challenges...</div>;
  }

  if (error) {
    return (
      <div className="challenge-list error">
        <p>❌ {error}</p>
        <button onClick={loadChallenges}>🔄 Retry</button>
      </div>
    );
  }

  if (challenges.length === 0) {
    return (
      <div className="challenge-list empty">
        <p>🎯 No challenges available yet.</p>
        <p className="hint">💡 Create a challenge using the API at http://127.0.0.1:8000/docs</p>
      </div>
    );
  }

  // Check if user completed all levels
  const allLevelsCompleted = userProgress?.level1_completed && userProgress?.level2_completed && userProgress?.level3_completed;

  if (showLeaderboard) {
    return <Leaderboard onClose={() => setShowLeaderboard(false)} />;
  }

  // Group challenges by their base name (without language suffix)
  const groupedChallenges = challenges.reduce((acc: any, challenge) => {
    const baseName = challenge.title.split(' - ')[0]; // e.g., "Armstrong Number"
    if (!acc[baseName]) {
      acc[baseName] = [];
    }
    acc[baseName].push(challenge);
    return acc;
  }, {});

  // Get unique challenge groups
  const challengeGroups = Object.entries(groupedChallenges);

  return (
    <div className="challenge-list">
      <div className="challenge-list-header">
        <h2>🎯 Available Challenges</h2>
        <div className="header-actions">
          <div className="level-selector">
            <button
              className={`level-btn ${selectedLevel === 1 ? 'active' : ''} ${user.current_level < 1 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(1)}
              disabled={user.current_level < 1}
            >
              🥉 Level 1 {user.current_level < 1 && '🔒'}
            </button>
            <button
              className={`level-btn ${selectedLevel === 2 ? 'active' : ''} ${user.current_level < 2 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(2)}
              disabled={user.current_level < 2}
            >
              🥈 Level 2 {user.current_level < 2 && '🔒'}
            </button>
            <button
              className={`level-btn ${selectedLevel === 3 ? 'active' : ''} ${user.current_level < 3 ? 'locked' : ''}`}
              onClick={() => setSelectedLevel(3)}
              disabled={user.current_level < 3}
            >
              🥇 Level 3 {user.current_level < 3 && '🔒'}
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
            <h2 className="thank-you-title">🌟 Thank You for Participating! 🌟</h2>
            <p className="thank-you-message">📢 The results will be declared soon.</p>
            <p className="thank-you-prize">🎁 You have a chance to win exciting prizes! 🏅</p>
          </div>
        </div>
      )}

      <div className="challenges-grid-new">
        {challengeGroups.map(([baseName, groupChallenges]: [string, any]) => (
          <ChallengeCard
            key={baseName}
            baseName={baseName}
            groupChallenges={groupChallenges}
            selectedLevel={selectedLevel}
            userProgress={userProgress}
            user={user}
            getChallengeStatus={getChallengeStatus}
            getStatusBadge={getStatusBadge}
            onSelectChallenge={onSelectChallenge}
            loadUserProgress={loadUserProgress}
          />
        ))}
      </div>
    </div>
  );
};

// Separate component for each challenge card to properly use hooks
interface ChallengeCardProps {
  baseName: string;
  groupChallenges: any[];
  selectedLevel: number;
  userProgress: UserProgress | null;
  user: UserResponse;
  getChallengeStatus: (challenge: Challenge) => string;
  getStatusBadge: (status: string) => JSX.Element;
  onSelectChallenge: (challenge: Challenge) => void;
  loadUserProgress: () => Promise<void>;
}

const ChallengeCard: React.FC<ChallengeCardProps> = ({
  baseName,
  groupChallenges,
  selectedLevel,
  userProgress,
  user,
  getChallengeStatus,
  getStatusBadge,
  onSelectChallenge,
  loadUserProgress,
}) => {
  const firstChallenge = groupChallenges[0];
  const status = getChallengeStatus(firstChallenge);
  const isCompleted = userProgress ? (
    (firstChallenge.level === 1 && userProgress.level1_completed) ||
    (firstChallenge.level === 2 && userProgress.level2_completed) ||
    (firstChallenge.level === 3 && userProgress.level3_completed)
  ) : false;

  // Get the selected language for this level
  const levelLanguage = selectedLevel === 1 ? userProgress?.level1_language :
                        selectedLevel === 2 ? userProgress?.level2_language :
                        userProgress?.level3_language;

  // Find the challenge for the selected language
  const selectedChallenge = levelLanguage 
    ? groupChallenges.find((c: any) => c.language === levelLanguage) || firstChallenge
    : firstChallenge;

  // Don't default to any language - user must select
  const [tempLanguage, setTempLanguage] = useState<string | null>(levelLanguage || null);
  const tempChallenge = tempLanguage 
    ? groupChallenges.find((c: any) => c.language === tempLanguage) || firstChallenge
    : firstChallenge;

  return (
    <div
      className={`challenge-card-new ${status} ${isCompleted ? 'completed' : ''}`}
    >
      <div className="challenge-card-header">
        <div className="challenge-title-section">
          <h3>{baseName}</h3>
          {isCompleted ? (
            <span className="badge badge-completed">Completed ✓</span>
          ) : (
            getStatusBadge(status)
          )}
        </div>
        
        {!isCompleted && !levelLanguage && (
          <div className="language-selector-inline">
            <label>💻 Select Language:</label>
            <div className="language-buttons">
              <button
                className={`lang-btn ${tempLanguage === 'python' ? 'active' : ''}`}
                onClick={() => setTempLanguage('python')}
              >
                🐍 Python
              </button>
              <button
                className={`lang-btn ${tempLanguage === 'c' ? 'active' : ''}`}
                onClick={() => setTempLanguage('c')}
              >
                ©️ C
              </button>
              <button
                className={`lang-btn ${tempLanguage === 'java' ? 'active' : ''}`}
                onClick={() => setTempLanguage('java')}
              >
                ☕ Java
              </button>
              <button
                className={`lang-btn ${tempLanguage === 'cpp' ? 'active' : ''}`}
                onClick={() => setTempLanguage('cpp')}
              >
                ⚡ C++
              </button>
            </div>
          </div>
        )}

        {levelLanguage && (
          <div className="selected-language-display">
            <span className="lang-label">💻 Language:</span>
            <span className="lang-value">{levelLanguage.toUpperCase()}</span>
            <span className="lang-locked">🔒 Locked</span>
          </div>
        )}
      </div>

      <p className="challenge-description-new">
        {tempLanguage ? tempChallenge.description : '👆 Please select a language above to view the challenge description'}
      </p>
      
      <div className="challenge-meta-new">
        <div className="meta-item">
          <span className="meta-icon">📦</span>
          <span>{tempLanguage ? (tempChallenge.fragments?.length || 0) : '?'} fragments</span>
        </div>
        <div className="meta-item">
          <span className="meta-icon">✓</span>
          <span>{tempLanguage ? (tempChallenge.test_cases?.length || 0) : '?'} tests</span>
        </div>
        <div className="meta-item">
          <span className="meta-icon">⏱️</span>
          <span>3 minutes</span>
        </div>
      </div>

      <button 
        className="start-button-new"
        onClick={async () => {
          if (!isCompleted) {
            if (!levelLanguage) {
              // Check if user selected a language
              if (!tempLanguage) {
                alert('⚠️ Please select a language first!');
                return;
              }
              // Save language selection first
              try {
                await apiClient.selectLanguage(user.id, selectedLevel, tempLanguage);
                await loadUserProgress();
                // Then start the challenge
                const challengeToStart = groupChallenges.find((c: any) => c.language === tempLanguage);
                onSelectChallenge(challengeToStart);
              } catch (err: any) {
                alert(err.message || 'Failed to select language');
              }
            } else {
              onSelectChallenge(selectedChallenge);
            }
          }
        }}
        disabled={isCompleted}
      >
        {isCompleted ? '✅ Completed' : '🚀 Start Challenge →'}
      </button>
    </div>
  );
};

export default ChallengeList;
