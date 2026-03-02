import React from "react";

interface ScoreGaugeProps {
  score: number;
}

const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score }) => {
  const radius = 80;
  const stroke = 10;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 75) return "#22c55e";
    if (s >= 50) return "#eab308";
    if (s >= 30) return "#f97316";
    return "#ef4444";
  };

  const getLabel = (s: number) => {
    if (s >= 75) return "Strong Match";
    if (s >= 50) return "Moderate Match";
    if (s >= 30) return "Partial Match";
    return "Weak Match";
  };

  const color = getColor(score);

  return (
    <div className="score-gauge">
      <svg height={radius * 2} width={radius * 2}>
        <circle
          stroke="rgba(255,255,255,0.08)"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference + " " + circumference}
          style={{
            strokeDashoffset,
            transition: "stroke-dashoffset 1.2s ease-out",
            transform: "rotate(-90deg)",
            transformOrigin: "50% 50%",
          }}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <div className="score-gauge__text">
        <span className="score-gauge__number" style={{ color }}>
          {score}
        </span>
        <span className="score-gauge__label">{getLabel(score)}</span>
      </div>
    </div>
  );
};

export default ScoreGauge;