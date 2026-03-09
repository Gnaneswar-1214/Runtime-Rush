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
  const [showLanguageSelector, setShowLanguageSelector] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');

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
      
      // Check if language is already selected for current level
      if (selectedLevel === 1 && progress.level1_language) {
        setSelectedLanguage(progress.level1_language);
      } else if (selectedLevel === 2 && progress.level2_language) {
        setSelectedLanguage(progress.level2_language);
      } else if (selectedLevel === 3 && progress.level3_language) {
        setSelectedLanguage(progress.level3_language);
      } else {
        setSelectedLanguage('');
      }
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
      
      // If language is selected, filter by language
      if (selectedLanguage) {
        const languageFiltered = filteredData.filter((c: any) => c.language === selectedLanguage);
        setChallenges(languageFiltered);
      } else {
        setChallenges(filteredData);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load challenges. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageSelect = async (language: string) => {
    try {
      await apiClient.selectLanguage(user.id, selectedLevel, language);
      setSelectedLanguage(language);
      setShowLanguageSelector(false);
      loadUserProgress();
      loadChallenges();
    } catch (err: any) {
      alert(err.message || 'Failed to select language');
    }
  };

  const handleStartChallenge = (challenge: Challenge) => {
    // Check if language is selected
    const languageSelected = 
      (selectedLevel === 1 && userProgress?.level1_language) ||
      (selectedLevel === 2 && userProgress?.level2_language) ||
      (selectedLevel === 3 && userProgress?.level3_language);
    
    if (!languageSelected) {
      setShowLanguageSelector(true);
      return;
    }
    
    onSelectChallenge(challenge);
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
      {showLanguageSelector && (
        <div className="language-selector-overlay">
          <div className="language-selector-modal">
            <h2>Select Programming Language</h2>
            <p>Choose a language for Level {selectedLevel}. You cannot change it later!</p>
            <div className="language-options">
              <button className="language-option" onClick={() => handleLanguageSelect('python')}>
                <span className="language-icon">🐍</span>
                <span className="language-name">Python</span>
              </button>
              <button className="language-option" onClick={() => handleLanguageSelect('c')}>
                <span className="language-icon">©️</span>
                <span className="language-name">C</span>
              </button>
              <button className="language-option" onClick={() => handleLanguageSelect('java')}>
                <span className="language-icon">☕</span>
                <span className="language-name">Java</span>
              </button>
              <button className="language-option" onClick={() => handleLanguageSelect('cpp')}>
                <span className="language-icon">⚡</span>
                <span className="language-name">C++</span>
              </button>
            </div>
            <button className="cancel-btn" onClick={() => setShowLanguageSelector(false)}>Cancel</button>
          </div>
        </div>
      )}

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

      {selectedLanguage && (
        <div className="selected-language-badge">
          <span className="badge-label">Selected Language:</span>
          <span className="badge-value">{selectedLanguage.toUpperCase()}</span>
        </div>
      )}

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
                onClick={() => !isCompleted && handleStartChallenge(challenge)}
                disabled={isCompleted}
              >
                {isCompleted ? 'Already Completed' : selectedLanguage ? 'Start Challenge →' : 'Select Language First'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ChallengeList;
