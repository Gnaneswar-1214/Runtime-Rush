import React, { useState, useEffect } from 'react';
import { Challenge, UserResponse, apiClient } from '../services/api';
import Leaderboard from './Leaderboard';
import './DragDropChallenge.css';

interface DragDropChallengeProps {
  challenge: Challenge;
  user: UserResponse;
  onBack: () => void;
  onComplete: () => void;
}

interface CodeFragment {
  id: string;
  content: string;
  order: number;
}

const DragDropChallenge: React.FC<DragDropChallengeProps> = ({ challenge, user, onBack, onComplete }) => {
  // Create a unique key for this challenge session
  const sessionKey = `challenge_${challenge.id}_${user.id}`;
  
  // Check if this challenge has been started before
  const getSessionData = () => {
    const saved = sessionStorage.getItem(sessionKey);
    if (saved) {
      return JSON.parse(saved);
    }
    return null;
  };

  const savedSession = getSessionData();
  const hasStarted = savedSession !== null;

  const [showPreviewText, setShowPreviewText] = useState(!hasStarted);
  const [showPreview, setShowPreview] = useState(false);
  const [showStart, setShowStart] = useState(false);
  const [previewTime, setPreviewTime] = useState(3);
  const [fragments, setFragments] = useState<CodeFragment[]>(savedSession?.fragments || []);
  const [dropZone, setDropZone] = useState<CodeFragment[]>(savedSession?.dropZone || []);
  const [draggedItem, setDraggedItem] = useState<CodeFragment | null>(null);
  const [timeLeft, setTimeLeft] = useState(savedSession?.timeLeft || 180);
  const [timerActive, setTimerActive] = useState(hasStarted);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [earnedScore, setEarnedScore] = useState(0);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [tabSwitchWarning, setTabSwitchWarning] = useState(false);

  // Tab switching detection
  useEffect(() => {
    if (!timerActive) return; // Only monitor when challenge is active

    const handleVisibilityChange = () => {
      if (document.hidden) {
        // User switched away from the tab
        setTimerActive(false); // Pause the timer
        setTabSwitchWarning(true); // Show warning
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [timerActive]);

  const handleTabSwitchOk = () => {
    // Just resume the challenge
    setTabSwitchWarning(false);
    setTimerActive(true); // Resume timer
  };

  useEffect(() => {
    if (!hasStarted) {
      // First time starting this challenge - shuffle fragments
      const shuffled = [...(challenge.fragments || [])].sort(() => Math.random() - 0.5);
      setFragments(shuffled);

      // Set timer to exactly 3 minutes (180 seconds)
      setTimeLeft(180);

      // Show "PREVIEW" text for 1.5 seconds, then show code preview
      setTimeout(() => {
        setShowPreviewText(false);
        setShowPreview(true);
      }, 1500);
    }
    // If hasStarted is true, we skip the preview and timer is already active
  }, [challenge, hasStarted]);

  // Save session data whenever state changes
  useEffect(() => {
    if (timerActive) {
      sessionStorage.setItem(sessionKey, JSON.stringify({
        fragments,
        dropZone,
        timeLeft,
        started: true
      }));
    }
  }, [fragments, dropZone, timeLeft, timerActive, sessionKey]);

  useEffect(() => {
    if (showPreview && previewTime > 0) {
      const timer = setTimeout(() => {
        setPreviewTime(previewTime - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (showPreview && previewTime === 0 && !hasStarted) {
      // Preview countdown finished, show START animation (only on first visit)
      setShowPreview(false);
      setShowStart(true);
      setTimeout(() => {
        setShowStart(false);
        setTimerActive(true);
      }, 1500);
    }
  }, [showPreview, previewTime, hasStarted]);

  useEffect(() => {
    if (timerActive && timeLeft > 0) {
      const timer = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timerActive && timeLeft === 0) {
      // Time is up - auto-submit with 0 score
      setTimerActive(false);
      handleTimeUp();
    }
  }, [timerActive, timeLeft]);

  const handleTimeUp = async () => {
    try {
      // Submit with time taken = 180 (full time), which gives 0 score
      const result = await apiClient.completeLevel(user.id, challenge.level || 1, 180);
      console.log('Time up - Level marked as completed with 0 score:', result);
      
      // Clear session data
      sessionStorage.removeItem(sessionKey);
      
      // Store the earned score (0)
      setEarnedScore(0);
      
      // Show success overlay with 0 marks
      setShowSuccess(true);
      
      // Auto-close after 3 seconds
      setTimeout(() => {
        onComplete();
      }, 3000);
    } catch (err) {
      console.error('Failed to complete level:', err);
      alert('Time is up!');
      onBack();
    }
  };

  const handleDragStart = (e: React.DragEvent, fragment: CodeFragment, fromDropZone: boolean) => {
    setDraggedItem(fragment);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('fromDropZone', fromDropZone.toString());
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDropInZone = (e: React.DragEvent, index?: number) => {
    e.preventDefault();
    if (!draggedItem) return;

    const fromDropZone = e.dataTransfer.getData('fromDropZone') === 'true';

    if (fromDropZone) {
      // Reorder within drop zone
      const newDropZone = dropZone.filter(f => f.id !== draggedItem.id);
      if (index !== undefined) {
        newDropZone.splice(index, 0, draggedItem);
      } else {
        newDropZone.push(draggedItem);
      }
      setDropZone(newDropZone);
    } else {
      // Add from fragments to drop zone
      setFragments(fragments.filter(f => f.id !== draggedItem.id));
      if (index !== undefined) {
        const newDropZone = [...dropZone];
        newDropZone.splice(index, 0, draggedItem);
        setDropZone(newDropZone);
      } else {
        setDropZone([...dropZone, draggedItem]);
      }
    }

    setDraggedItem(null);
  };

  const handleDropBackToFragments = (e: React.DragEvent) => {
    e.preventDefault();
    if (!draggedItem) return;

    const fromDropZone = e.dataTransfer.getData('fromDropZone') === 'true';
    if (fromDropZone) {
      setDropZone(dropZone.filter(f => f.id !== draggedItem.id));
      setFragments([...fragments, draggedItem]);
    }

    setDraggedItem(null);
  };

  const handleSubmit = async () => {
    // Check if order is correct
    const isCorrect = dropZone.every((fragment, index) => fragment.order === index + 1);

    if (isCorrect) {
      // Calculate time taken (180 seconds - remaining time)
      const timeTaken = 180 - timeLeft;
      
      // Stop the timer immediately
      setTimerActive(false);
      
      // Complete level with time taken
      try {
        const result = await apiClient.completeLevel(user.id, challenge.level || 1, timeTaken);
        console.log('Level completed:', result);
        
        // Clear session data on successful completion
        sessionStorage.removeItem(sessionKey);
        
        // Store the earned score
        setEarnedScore(result.score);
        
        // If level 3 completed, show thank you message (no auto-close)
        if (challenge.level === 3) {
          setShowSuccess(true);
          // Don't auto-close, user will see leaderboard button
        } else {
          // For levels 1 and 2, show success briefly then move to next level
          setShowSuccess(true);
          setTimeout(() => {
            onComplete();
          }, 3000);
        }
      } catch (err) {
        console.error('Failed to complete level:', err);
        setShowError(true);
        setTimeout(() => setShowError(false), 2000);
      }
    } else {
      setShowError(true);
      setTimeout(() => setShowError(false), 2000);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (showLeaderboard) {
    return <Leaderboard onClose={onBack} />;
  }

  // Don't show preview if success overlay is showing
  if (showSuccess) {
    return (
      <div className="success-overlay">
        <div className="success-animation">
          {challenge.level === 3 ? (
            // Level 3 completion - Simple completion message
            <>
              <div className="success-checkmark">🏆</div>
              <h2 className="final-title">Level 3 Complete!</h2>
              <p className="score-display">You earned: <strong>{earnedScore.toFixed(2)}</strong> marks</p>
              <button className="view-leaderboard-btn" onClick={() => {
                setShowSuccess(false);
                setShowLeaderboard(true);
              }}>
                View Leaderboard
              </button>
              <button className="back-to-home-btn" onClick={onBack}>
                Back to Home
              </button>
            </>
          ) : (
            // Levels 1 and 2 completion
            <>
              <div className="success-checkmark">✓</div>
              <h2>Level {challenge.level} Complete! 🎉</h2>
              <p className="score-display">You earned: <strong>{earnedScore.toFixed(2)}</strong> marks</p>
              <p>Moving to next level...</p>
            </>
          )}
        </div>
      </div>
    );
  }

  if (showPreviewText) {
    return (
      <div className="preview-text-container">
        <div className="preview-text-animation">
          <div className="preview-text-main">PREVIEW</div>
          <div className="preview-text-subtitle">Get ready to memorize the solution</div>
        </div>
      </div>
    );
  }

  if (showPreview) {
    return (
      <div className="preview-container">
        <div className="preview-overlay">
          <div className="preview-badge">PREVIEW</div>
          <div className="preview-content">
            <div className="preview-header">
              <h2>📖 Study the Solution</h2>
              <p className="preview-subtitle">Memorize the correct order before the challenge begins</p>
            </div>
            <div className="preview-timer-circle">
              <svg className="timer-ring" viewBox="0 0 120 120">
                <circle className="timer-ring-bg" cx="60" cy="60" r="54" />
                <circle 
                  className="timer-ring-progress" 
                  cx="60" 
                  cy="60" 
                  r="54"
                  style={{
                    strokeDasharray: `${(previewTime / 3) * 339.292} 339.292`,
                    transform: 'rotate(-90deg)',
                    transformOrigin: '50% 50%'
                  }}
                />
              </svg>
              <div className="timer-text">
                <span className="timer-number">{previewTime}</span>
                <span className="timer-label">seconds</span>
              </div>
            </div>
            <div className="preview-code">
              {challenge.fragments
                ?.sort((a, b) => a.order - b.order)
                .map((fragment, index) => (
                  <div key={fragment.id} className="preview-fragment">
                    <span className="fragment-number">{index + 1}</span>
                    <pre>{fragment.content}</pre>
                  </div>
                ))}
            </div>
            <div className="preview-hint">
              <span className="hint-icon">💡</span>
              <span>Pay attention to the order - you'll need to arrange these correctly!</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (showStart) {
    return (
      <div className="start-container">
        <div className="start-animation">
          <div className="start-text">START!</div>
          <div className="start-subtitle">Arrange the code fragments now</div>
        </div>
      </div>
    );
  }

  return (
    <div className="drag-drop-challenge">
      {tabSwitchWarning && (
        <div className="tab-switch-overlay">
          <div className="tab-switch-warning">
            <div className="warning-icon">⚠️</div>
            <h2>Tab Switch Detected!</h2>
            <p>You switched to another tab or window during the challenge.</p>
            <p className="warning-consequence">Please stay on this page to continue.</p>
            <button className="warning-ok-button" onClick={handleTabSwitchOk}>
              OK - Resume Challenge
            </button>
          </div>
        </div>
      )}

      {showError && (
        <div className="error-overlay">
          <div className="error-animation">
            <div className="error-mark">✗</div>
            <h2>Incorrect Order</h2>
            <p>Try again!</p>
          </div>
        </div>
      )}

      <div className="challenge-header">
        <img src="/logo-jntu.png" alt="JNTU Logo" className="challenge-logo challenge-logo-left" />
        
        <button className="back-button" onClick={onBack}>← Back</button>
        <h1>{challenge.title}</h1>
        <div className="timer-display">
          <span className="timer-icon">⏱️</span>
          <span className={`timer-value ${timeLeft < 60 ? 'warning' : ''}`}>
            {formatTime(timeLeft)}
          </span>
        </div>
        
        <img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="challenge-logo challenge-logo-right" />
      </div>

      <div className="challenge-description">
        <p>{challenge.description}</p>
        <p className="instruction">Drag the code fragments in the correct order!</p>
      </div>

      <div className="challenge-workspace">
        <div className="fragments-panel">
          <h3>Code Fragments</h3>
          <div
            className="fragments-container"
            onDragOver={handleDragOver}
            onDrop={handleDropBackToFragments}
          >
            {fragments.map((fragment) => (
              <div
                key={fragment.id}
                className="code-fragment"
                draggable
                onDragStart={(e) => handleDragStart(e, fragment, false)}
              >
                <div className="fragment-handle">⋮⋮</div>
                <pre>{fragment.content}</pre>
              </div>
            ))}
            {fragments.length === 0 && (
              <div className="empty-message">All fragments used!</div>
            )}
          </div>
        </div>

        <div className="drop-zone-panel">
          <h3>Your Solution</h3>
          <div className="drop-zone" onDragOver={handleDragOver} onDrop={(e) => handleDropInZone(e)}>
            {dropZone.map((fragment, index) => (
              <div key={fragment.id} className="drop-zone-item">
                <div
                  className="dropped-fragment"
                  draggable
                  onDragStart={(e) => handleDragStart(e, fragment, true)}
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDropInZone(e, index)}
                >
                  <div className="fragment-number">{index + 1}</div>
                  <div className="fragment-handle">⋮⋮</div>
                  <pre>{fragment.content}</pre>
                </div>
              </div>
            ))}
            {dropZone.length === 0 && (
              <div className="drop-placeholder">
                Drop code fragments here in the correct order
              </div>
            )}
          </div>

          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={dropZone.length !== (challenge.fragments?.length || 0)}
          >
            Submit Solution
          </button>
        </div>
      </div>
    </div>
  );
};

export default DragDropChallenge;
