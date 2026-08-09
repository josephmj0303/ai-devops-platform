import api from "./axios";

import type {
  AIChatResponse,
  DockerReviewResponse,
  KubernetesReviewResponse,
  TerraformReviewResponse,
  LogExplanationResponse,
} from "../types/ai";

export const chat = async (
  prompt: string
): Promise<AIChatResponse> => {
  const response = await api.post<AIChatResponse>(
    "/ai/chat",
    {
      prompt,
    }
  );

  return response.data;
};

export const reviewDockerfile = async (
  dockerfile: string
): Promise<DockerReviewResponse> => {
  const response = await api.post<DockerReviewResponse>(
    "/ai/review/dockerfile",
    {
      dockerfile,
    }
  );

  return response.data;
};

export const reviewKubernetes = async (
  manifest: string
): Promise<KubernetesReviewResponse> => {
  const response =
    await api.post<KubernetesReviewResponse>(
      "/ai/review/kubernetes",
      {
        manifest,
      }
    );

  return response.data;
};

export const reviewTerraform = async (
  terraform: string
): Promise<TerraformReviewResponse> => {
  const response =
    await api.post<TerraformReviewResponse>(
      "/ai/review/terraform",
      {
        terraform,
      }
    );

  return response.data;
};

export const explainLog = async (
  logs: string
): Promise<LogExplanationResponse> => {
  const response =
    await api.post<LogExplanationResponse>(
      "/ai/explain/log",
      {
        logs,
      }
    );

  return response.data;
};
