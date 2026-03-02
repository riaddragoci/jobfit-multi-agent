export interface Project {
  title: string;
  technologies: string[];
  bullets: string[];
}

export interface Experience {
  title: string;
  org: string;
  dates: string;
  bullets: string[];
}

export interface JDData {
  role_title: string;
  seniority_level: string;
  required_skills: string[];
  preferred_skills: string[];
  key_keywords: string[];
  responsibilities: string[];
  red_flags: string[];
}

export interface CVData {
  candidate_name: string;
  summary: string;
  skills: string[];
  coursework: string[];
  projects: Project[];
  experience: Experience[];
  achievements: string[];
}

export interface MatchData {
  score: number;
  required_hit: string[];
  required_missing: string[];
  keywords_hit: string[];
  red_flags_missing: string[];
}

export interface AdviceData {
  summary: string;
  strengths: string[];
  gaps: string[];
  next_actions: string[];
}

export interface ProjectBullet {
  project: string;
  bullets: string[];
}

export interface RewriteData {
  headline: string;
  summary: string;
  project_bullets: ProjectBullet[];
  skills: string[];
  notes: string[];
}

export interface AnalyzeResponse {
  jd_data: JDData;
  cv_data: CVData;
  match_data: MatchData;
  advice_data: AdviceData;
  rewrite_data: RewriteData;
}