import React from 'react';

function StatCard({ label, value, icon, change }) {
  let changeClass = '';
  let changePrefix = '';

  if (change !== undefined && change !== null) {
    if (change > 0) {
      changeClass = 'stat-card__change stat-card__change--up';
      changePrefix = '+';
    } else if (change < 0) {
      changeClass = 'stat-card__change stat-card__change--down';
      changePrefix = '';
    } else {
      changeClass = 'stat-card__change';
      changePrefix = '';
    }
  }

  return (
    <div className="stat-card">
      {icon && <div className="stat-card__icon">{icon}</div>}
      <div className="stat-card__label">{label}</div>
      <div className="stat-card__value">{value}</div>
      {change !== undefined && change !== null && (
        <div className={changeClass}>
          {changePrefix}{typeof change === 'number' ? change.toFixed(2) : change}%
        </div>
      )}
    </div>
  );
}

export default StatCard;
