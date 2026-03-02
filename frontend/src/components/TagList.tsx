import React from "react";

interface TagListProps {
  items: string[];
  variant?: "hit" | "miss" | "neutral" | "keyword";
}

const TagList: React.FC<TagListProps> = ({ items, variant = "neutral" }) => {
  if (!items || items.length === 0) return <p className="tag-list__empty">None</p>;

  return (
    <div className="tag-list">
      {items.map((item, i) => (
        <span key={i} className={`tag tag--${variant}`}>
          {variant === "hit" && <span className="tag__icon">✓</span>}
          {variant === "miss" && <span className="tag__icon">✗</span>}
          {item}
        </span>
      ))}
    </div>
  );
};

export default TagList;