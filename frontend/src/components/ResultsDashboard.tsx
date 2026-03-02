import React from "react";
import { AnalyzeResponse } from "../types";
import ScoreGauge from "./ScoreGauge";
import TagList from "./TagList";
import SectionCard from "./SectionCard";

interface ResultsDashboardProps {
  data: AnalyzeResponse;
  onReset: () => void;
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ data, onReset }) => {
  const { jd_data, cv_data, match_data, advice_data, rewrite_data } = data;

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard__header">
        <div className="dashboard__header-info">
          <h2 className="dashboard__candidate">{cv_data.candidate_name || "Candidate"}</h2>
          <p className="dashboard__role">
            {jd_data.role_title || "Role"}{" "}
            <span className="dashboard__seniority">
              ({jd_data.seniority_level || "unspecified"})
            </span>
          </p>
        </div>
        <button onClick={onReset} className="dashboard__reset-btn">
          ← New Analysis
        </button>
      </div>

      {/* Score + Overview Row */}
      <div className="dashboard__score-row">
        <div className="dashboard__score-card">
          <ScoreGauge score={match_data.score} />
        </div>

        <div className="dashboard__overview-card">
          <SectionCard title="Summary" icon="📋">
            <p className="dashboard__summary-text">
              {advice_data.summary || "No summary generated."}
            </p>
            <div className="dashboard__stats">
              <div className="dashboard__stat">
                <span className="dashboard__stat-number dashboard__stat-number--green">
                  {match_data.required_hit?.length || 0}
                </span>
                <span className="dashboard__stat-label">Skills Matched</span>
              </div>
              <div className="dashboard__stat">
                <span className="dashboard__stat-number dashboard__stat-number--red">
                  {match_data.required_missing?.length || 0}
                </span>
                <span className="dashboard__stat-label">Skills Missing</span>
              </div>
              <div className="dashboard__stat">
                <span className="dashboard__stat-number dashboard__stat-number--blue">
                  {match_data.keywords_hit?.length || 0}
                </span>
                <span className="dashboard__stat-label">Keywords Hit</span>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>

      {/* Skills Breakdown */}
      <div className="dashboard__grid-2">
        <SectionCard title="Matched Requirements" icon="✅">
          <TagList items={match_data.required_hit} variant="hit" />
        </SectionCard>

        <SectionCard title="Missing Requirements" icon="⚠️">
          <TagList items={match_data.required_missing} variant="miss" />
        </SectionCard>
      </div>

      {/* Keywords + Red Flags */}
      <div className="dashboard__grid-2">
        <SectionCard title="Keywords Matched" icon="🔑">
          <TagList items={match_data.keywords_hit} variant="keyword" />
        </SectionCard>

        <SectionCard title="Red Flags Missing" icon="🚩">
          <TagList items={match_data.red_flags_missing} variant="miss" />
        </SectionCard>
      </div>

      {/* Advice Section */}
      <div className="dashboard__grid-3">
        <SectionCard title="Strengths" icon="💪">
          <ul className="dashboard__list">
            {(advice_data.strengths || []).map((s, i) => (
              <li key={i} className="dashboard__list-item dashboard__list-item--green">
                {s}
              </li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Gaps to Address" icon="📌">
          <ul className="dashboard__list">
            {(advice_data.gaps || []).map((g, i) => (
              <li key={i} className="dashboard__list-item dashboard__list-item--amber">
                {g}
              </li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard title="Next Actions" icon="🚀">
          <ul className="dashboard__list">
            {(advice_data.next_actions || []).map((a, i) => (
              <li key={i} className="dashboard__list-item dashboard__list-item--blue">
                {a}
              </li>
            ))}
          </ul>
        </SectionCard>
      </div>

      {/* CV Rewrite Section */}
      <SectionCard title="CV Rewrite Suggestions" icon="✏️" className="dashboard__rewrite">
        {rewrite_data.headline && (
          <div className="dashboard__rewrite-section">
            <h4 className="dashboard__rewrite-label">Suggested Headline</h4>
            <p className="dashboard__rewrite-headline">{rewrite_data.headline}</p>
          </div>
        )}

        {rewrite_data.summary && (
          <div className="dashboard__rewrite-section">
            <h4 className="dashboard__rewrite-label">Suggested Summary</h4>
            <p className="dashboard__rewrite-text">{rewrite_data.summary}</p>
          </div>
        )}

        {(rewrite_data.project_bullets || []).length > 0 && (
          <div className="dashboard__rewrite-section">
            <h4 className="dashboard__rewrite-label">Rewritten Project Bullets</h4>
            {rewrite_data.project_bullets.map((proj, i) => (
              <div key={i} className="dashboard__rewrite-project">
                <h5 className="dashboard__rewrite-project-title">{proj.project}</h5>
                <ul className="dashboard__rewrite-bullets">
                  {(proj.bullets || []).map((b, j) => (
                    <li key={j}>{b}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {(rewrite_data.skills || []).length > 0 && (
          <div className="dashboard__rewrite-section">
            <h4 className="dashboard__rewrite-label">Suggested Skills</h4>
            <TagList items={rewrite_data.skills} variant="neutral" />
          </div>
        )}

        {(rewrite_data.notes || []).length > 0 && (
          <div className="dashboard__rewrite-section">
            <h4 className="dashboard__rewrite-label">Notes (Gaps to Address)</h4>
            <ul className="dashboard__list">
              {rewrite_data.notes.map((n, i) => (
                <li key={i} className="dashboard__list-item dashboard__list-item--amber">
                  {n}
                </li>
              ))}
            </ul>
          </div>
        )}
      </SectionCard>

      {/* Interpretation */}
      <div className="dashboard__footnote">
        <p>
          <strong>Note:</strong> This score reflects alignment to this specific JD, not overall
          ability. Low scores are common for highly specialized roles. Missing items are treated as
          gaps — no experience is assumed.
        </p>
      </div>
    </div>
  );
};

export default ResultsDashboard;