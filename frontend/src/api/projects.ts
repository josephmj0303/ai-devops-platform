import api from "./axios";
import type { Project, ProjectCreate } from "../types/project";

export const getProjects = async (): Promise<Project[]> => {
  const response = await api.get<Project[]>("/projects");
  return response.data;
};

export const createProject = async (
  project: ProjectCreate
): Promise<Project> => {
  const response = await api.post<Project>("/projects", project);
  return response.data;
};
