export interface AIChatRequest {
  prompt: string;
  system_prompt?: string;
}

export interface AIChatResponse {
  response: string;
}

export interface DockerReviewResponse {
  review: string;
}

export interface KubernetesReviewResponse {
  review: string;
}

export interface TerraformReviewResponse {
  review: string;
}

export interface LogExplanationResponse {
  explanation: string;
}

export type AnalysisSeverity =
  | "low"
  | "medium"
  | "high"
  | "critical";

export interface DevOpsAnalysisResponse {
  severity: AnalysisSeverity;
  component: string;
  summary: string;
  findings?: string[];
  likely_cause?: string;
  impact?: string;
  recommended_actions: string[];
}

export interface LogAnalysisResponse {
  severity: AnalysisSeverity;
  component: string;
  summary: string;
  likely_cause: string;
  impact: string;
  recommended_actions: string[];
}

export interface DockerAnalysisResponse
  extends DevOpsAnalysisResponse {
  findings: string[];
}

export interface KubernetesAnalysisResponse
  extends DevOpsAnalysisResponse {
  findings: string[];
}

export interface TerraformAnalysisResponse
  extends DevOpsAnalysisResponse {
  findings: string[];
}

export interface AIAnalysisHistoryItem {
  id: number;
  user_id: string;
  analysis_type: AnalysisType;
  input_text: string;
  result: {
    severity: AnalysisSeverity;
    component: string;
    summary: string;
    likely_cause?: string;
    impact?: string;
    findings?: string[];
    recommended_actions: string[];
  };
  created_at: string;
}

export type AnalysisType =
  | "logs"
  | "dockerfile"
  | "kubernetes"
  | "terraform";

export interface DockerContainer {
  name: string;
  status: string;
  image: string;
}

export interface AvailableAction {
  action: string;
  name: string;
  description: string;
  target_type: string;
  enabled: boolean;
}

export interface AvailableActionsResponse {
  component: string;
  actions: AvailableAction[];
}

export interface DevOpsActionResponse {
  action: string;
  target: string;
  status: string;
  message: string;
}
