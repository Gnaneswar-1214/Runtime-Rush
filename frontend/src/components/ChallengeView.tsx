import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { apiClient, Challenge, Submission } from '../services/api';
import Timer from './Timer';
import './ChallengeView.css';

interface ChallengeViewProps {
  challenge: Challenge;
  onBack: () => void;
}

const ChallengeView: React.FC<ChallengeViewProps> = ({ challenge, onBack }) => {
  const [code, setCode] = useState('');
  const [participantId] = useState('participant-' + Math.random().toString(36).substr(2, 9));
  const [submitting, setSubmitting] = useState(false);
  const [lastSubmission, setLastSubmission] = useState<Submission | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [confetti, setConfetti] = useState(false);

  useEffect(() => {
    // Initialize code with scrambled fragments
    if (challenge.fragments && challenge.fragments.length > 0) {
      const fragmentsCode = challenge.fragments
        .map(f => `# Fragment ${f.order}\n${f.content}`)
        .join('\n\n');
      setCode(fragmentsCode);
    }
  }, [challenge]);

  const handleSubmit = async () => {
    if (!code.trim()) {
      setError('Please write some code before submitting');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);
      
      // Mock submission for now (since we don't have submission endpoint)
      // In real implementation, this would call the API
      const mockSubmission: Submission = {
        id: Math.random().toString(36),
        challenge_id: challenge.id,
        participant_id: participantId,
        code: code,
        timestamp: new Date().toISOString(),
        is_correct: true, // Mock: assume correct for demo
        validation_result: {
          is_valid: true,
          syntax_errors: [],
          test_results: challenge.test_cases?.map(tc => ({
            test_case_id: tc.id,
            passed: true,
            actual_output: tc.expected_output,
            expected_output: tc.expected_output,
            execution_time: Math.random() * 100
          })) || [],
          all_tests_passed: true
        }
      };

      setLastSubmission(mockSubmission);
      
      if (mockSubmission.is_correct) {
        // Show success animation
        setShowSuccess(true);
        setConfetti(true);
        
        // Auto-advance after 3 seconds
        setTimeout(() => {
          setShowSuccess(false);
          setShowResults(true);
        }, 3000);
        
        // Stop confetti after 5 seconds
        setTimeout(() => {
          setConfetti(false);
        }, 5000);
      } else {
        setShowResults(true);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to submit code');
    } finally {
      setSubmitting(false);
    }
  };

  const getChallengeStatus = (): 'not-started' | 'active' | 'ended' => {
    const now = new Date();
    const start = new Date(challenge.start_time);
    const end = new Date(challenge.end_time);

    if (now < start) return 'not-started';
    if (now > end) return 'ended';
    return 'active';
  };

  const status = getChallengeStatus();
  const canSubmit = status === 'active';

  return (
    <div className="challenge-view">
      {confetti && <div className="confetti-container">
        {[...Array(50)].map((_, i) => (
          <div key={i} className="confetti" style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'][Math.floor(Math.random() * 5)]
          }}></div>
        ))}
      </div>}

      {showSuccess && (
        <div className="success-overlay">
          <div className="success-animation">
            <div className="success-checkmark">✓</div>
            <h2>Correct! 🎉</h2>
            <p>Moving to next challenge...</p>
          </div>
        </div>
      )}

      <div className="challenge-header">
        <button className="back-button" onClick={onBack}>← Back to Challenges</button>
        <h1>{challenge.title}</h1>
        <Timer startTime={challenge.start_time} endTime={challenge.end_time} />
      </div>

      <div className="challenge-content">
        <div className="challenge-info">
          <div className="info-section">
            <h3>Description</h3>
            <p>{challenge.description}</p>
          </div>

          <div className="info-section">
            <h3>Instructions</h3>
            <ul>
              <li>Reconstruct the code from the scrambled fragments</li>
              <li>Fix any bugs in the code</li>
              <li>Make sure all test cases pass</li>
              <li>Submit your solution before time runs out</li>
            </ul>
          </div>

          {challenge.test_cases && challenge.test_cases.filter(tc => tc.visible).length > 0 && (
            <div className="info-section">
              <h3>Visible Test Cases</h3>
              {challenge.test_cases.filter(tc => tc.visible).map((tc, idx) => (
                <div key={tc.id} className="test-case">
                  <strong>Test {idx + 1}:</strong>
                  <div className="test-input">Input: {tc.input || '(empty)'}</div>
                  <div className="test-output">Expected: {tc.expected_output}</div>
                </div>
              ))}
            </div>
          )}

          <div className="info-section meta">
            <div><strong>Language:</strong> {challenge.language}</div>
            <div><strong>Fragments:</strong> {challenge.fragments?.length || 0}</div>
            <div><strong>Total Tests:</strong> {challenge.test_cases?.length || 0}</div>
          </div>
        </div>

        <div className="editor-section">
          <div className="editor-header">
            <h3>Code Editor</h3>
            <div className="editor-actions">
              <span className="participant-id">ID: {participantId}</span>
              <button
                className="submit-button"
                onClick={handleSubmit}
                disabled={!canSubmit || submitting}
              >
                {submitting ? 'Submitting...' : 'Submit Solution'}
              </button>
            </div>
          </div>

          {!canSubmit && (
            <div className={`status-banner ${status}`}>
              {status === 'not-started' && 'Challenge has not started yet'}
              {status === 'ended' && 'Challenge has ended'}
            </div>
          )}

          {error && (
            <div className="error-banner">
              {error}
            </div>
          )}

          <Editor
            height="500px"
            defaultLanguage={challenge.language}
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              automaticLayout: true,
            }}
          />
        </div>
      </div>

      {showResults && lastSubmission && (
        <div className="results-modal">
          <div className="results-content">
            <button className="close-button" onClick={() => setShowResults(false)}>×</button>
            <h2>Submission Results</h2>
            
            <div className={`result-status ${lastSubmission.is_correct ? 'success' : 'failure'}`}>
              {lastSubmission.is_correct ? '✓ All Tests Passed!' : '✗ Some Tests Failed'}
            </div>

            <div className="submission-info">
              <div><strong>Submission ID:</strong> {lastSubmission.id}</div>
              <div><strong>Timestamp:</strong> {new Date(lastSubmission.timestamp).toLocaleString()}</div>
            </div>

            {lastSubmission.validation_result.syntax_errors.length > 0 && (
              <div className="syntax-errors">
                <h3>Syntax Errors</h3>
                {lastSubmission.validation_result.syntax_errors.map((err: any, idx: number) => (
                  <div key={idx} className="error-item">
                    Line {err.line}: {err.message}
                  </div>
                ))}
              </div>
            )}

            {lastSubmission.validation_result.test_results.length > 0 && (
              <div className="test-results">
                <h3>Test Results</h3>
                {lastSubmission.validation_result.test_results.map((result, idx) => (
                  <div key={idx} className={`test-result ${result.passed ? 'passed' : 'failed'}`}>
                    <div className="test-header">
                      <span>{result.passed ? '✓' : '✗'} Test {idx + 1}</span>
                      <span className="execution-time">{result.execution_time.toFixed(2)}ms</span>
                    </div>
                    {!result.passed && (
                      <div className="test-details">
                        <div><strong>Expected:</strong> {result.expected_output}</div>
                        <div><strong>Actual:</strong> {result.actual_output}</div>
                        {result.error && <div className="error">{result.error}</div>}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {lastSubmission.is_correct && (
              <button className="next-challenge-button" onClick={onBack}>
                Next Challenge →
              </button>
            )}

            <button className="close-modal-button" onClick={() => setShowResults(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChallengeView;
