import React from 'react';
import SentimentBadge from './SentimentBadge';

function NewsCard({ article }) {
  const {
    title,
    description,
    source,
    published_at,
    url,
    sentiment_label,
    sentiment_score,
  } = article;

  const formattedDate = published_at
    ? new Date(published_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : '';

  return (
    <div className="news-card">
      <div className="news-card__header">
        <h3 className="news-card__title">
          {url ? (
            <a href={url} target="_blank" rel="noopener noreferrer">
              {title}
            </a>
          ) : (
            title
          )}
        </h3>
        <SentimentBadge sentiment_label={sentiment_label} score={sentiment_score} />
      </div>
      {description && (
        <p className="news-card__description">{description}</p>
      )}
      <div className="news-card__footer">
        <span className="news-card__source">{source || 'Unknown'}</span>
        <span>{formattedDate}</span>
      </div>
    </div>
  );
}

export default NewsCard;
