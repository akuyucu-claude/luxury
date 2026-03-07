import React from 'react';

function SentimentBadge({ sentiment_label, score }) {
  const label = (sentiment_label || 'neutral').toLowerCase();
  let className = 'sentiment-badge sentiment-badge--neutral';

  if (label === 'positive') {
    className = 'sentiment-badge sentiment-badge--positive';
  } else if (label === 'negative') {
    className = 'sentiment-badge sentiment-badge--negative';
  }

  return (
    <span className={className}>
      <span className={`sentiment-dot sentiment-dot--${label}`} />
      {label}{score !== undefined && score !== null ? ` (${Number(score).toFixed(2)})` : ''}
    </span>
  );
}

export default SentimentBadge;
