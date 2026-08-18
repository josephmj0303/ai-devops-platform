import api from "./axios";

import type {
  AIChatResponse,
  DockerReviewResponse,
  KubernetesReviewResponse,
  TerraformReviewResponse,
  LogExplanationResponse,
  LogAnalysisResponse,
  DockerAnalysisResponse,
  KubernetesAnalysisResponse,
  TerraformAnalysisResponse,
  AIAnalysisHistoryItem,
  DockerContainer,
  AvailableActionsResponse,
  DevOpsActionResponse,
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

/* Structured AI analysis */

export const analyzeLogs = async (
  logs: string
): Promise<LogAnalysisResponse> => {
  const response =
    await api.post<LogAnalysisResponse>(
      "/ai/analyze/logs",
      {
        logs,
      }
    );

  return response.data;
};

export const analyzeDockerfile = async (
  dockerfile: string
): Promise<DockerAnalysisResponse> => {
  const response =
    await api.post<DockerAnalysisResponse>(
      "/ai/analyze/dockerfile",
      {
        dockerfile,
      }
    );

  return response.data;
};

export const analyzeKubernetes = async (
  manifest: string
): Promise<KubernetesAnalysisResponse> => {
  const response =
    await api.post<KubernetesAnalysisResponse>(
      "/ai/analyze/kubernetes",
      {
        manifest,
      }
    );

  return response.data;
};

export const analyzeTerraform = async (
  terraform: string
): Promise<TerraformAnalysisResponse> => {
  const response =
    await api.post<TerraformAnalysisResponse>(
      "/ai/analyze/terraform",
      {
        terraform,
      }
    );

  return response.data;
};

export const getAnalysisHistory = async (): Promise<
  AIAnalysisHistoryItem[]
> => {
  const response = await api.get<AIAnalysisHistoryItem[]>(
    "/ai/history"
  );

  return response.data;
};

export const getDockerContainers = async (): Promise<
  DockerContainer[]
> => {
  const response = await api.get<DockerContainer[]>(
    "/ai/actions/docker/containers"
  );

  return response.data;
};

export const getAvailableActions = async (
  component: string
): Promise<AvailableActionsResponse> => {
  const response = await api.get<AvailableActionsResponse>(
    `/ai/actions/available/${component}`
  );

  return response.data;
};

export const restartDockerContainer = async (
  analysisId: number,
  containerName: string
): Promise<DevOpsActionResponse> => {
  const response = await api.post<DevOpsActionResponse>(
    "/ai/actions/docker/restart",
    {
      analysis_id: analysisId,
      container_name: containerName,
    }
  );

  return response.data;
};
