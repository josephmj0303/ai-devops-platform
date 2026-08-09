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
