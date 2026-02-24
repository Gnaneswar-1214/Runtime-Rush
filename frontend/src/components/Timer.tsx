import React, { useState, useEffect } from 'react';
import './Timer.css';

interface TimerProps {
  startTime: string;
  endTime: string;
}

const Timer: React.FC<TimerProps> = ({ startTime, endTime }) => {
  const [timeLeft, setTimeLeft] = useState<string>('');
  const [status, setStatus] = useState<'not-started' | 'active' | 'ended'>('not-started');

  useEffect(() => {
    const updateTimer = () => {
      const now = new Date();
      const start = new Date(startTime);
      const end = new Date(endTime);

      if (now < start) {
        setStatus('not-started');
        const diff = start.getTime() - now.getTime();
        setTimeLeft(formatTime(diff));
      } else if (now > end) {
        setStatus('ended');
        setTimeLeft('Challenge Ended');
      } else {
        setStatus('active');
        const diff = end.getTime() - now.getTime();
        setTimeLeft(formatTime(diff));
      }
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [startTime, endTime]);

  const formatTime = (ms: number): string => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) {
      return `${days}d ${hours % 24}h ${minutes % 60}m`;
    } else if (hours > 0) {
      return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    } else {
      return `${seconds}s`;
    }
  };

  return (
    <div className={`timer ${status}`}>
      <div className="timer-label">
        {status === 'not-started' && 'Starts in:'}
        {status === 'active' && 'Time Remaining:'}
        {status === 'ended' && ''}
      </div>
      <div className="timer-value">{timeLeft}</div>
    </div>
  );
};

export default Timer;
