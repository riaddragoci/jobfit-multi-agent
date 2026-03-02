import React from "react";

interface SectionCardProps {
  title: string;
  icon?: string;
  children: React.ReactNode;
  className?: string;
}

const SectionCard: React.FC<SectionCardProps> = ({
  title,
  icon,
  children,
  className = "",
}) => {
  return (
    <div className={`section-card ${className}`}>
      <div className="section-card__header">
        {icon && <span className="section-card__icon">{icon}</span>}
        <h3 className="section-card__title">{title}</h3>
      </div>
      <div className="section-card__body">{children}</div>
    </div>
  );
};

export default SectionCard;