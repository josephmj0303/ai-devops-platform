import { useEffect, useState } from "react";

import {
  chat,
  reviewDockerfile,
  reviewKubernetes,
  reviewTerraform,
  explainLog,
} from "../api/ai";

import { getProjects } from "../api/projects";
import type { Project } from "../types/project";

type Operation =
  | "chat"
  | "dockerfile"
  | "kubernetes"
  | "terraform"
  | "log";

export default function AIAssistant() {
  const [operation, setOperation] =
    useState<Operation>("log");

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] =
    useState("");

  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const [loading, setLoading] = useState(false);
  const [loadingProjects, setLoadingProjects] =
    useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    const loadProjects = async () => {
      try {
        const data = await getProjects();

        setProjects(data);

        if (data.length > 0) {
          setSelectedProject(String(data[0].id));
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load projects.");
      } finally {
        setLoadingProjects(false);
      }
    };

    loadProjects();
  }, []);

  const getPlaceholder = () => {
    switch (operation) {
      case "chat":
        return "Describe your DevOps problem or question...";

      case "dockerfile":
        return "Paste your Dockerfile here...";

      case "kubernetes":
        return "Paste your Kubernetes manifest here...";

      case "terraform":
        return "Paste your Terraform configuration here...";

      case "log":
        return "Paste your application logs here...";
    }
  };

  const getResponseTitle = () => {
    switch (operation) {
      case "chat":
        return "AI Response";

      case "dockerfile":
        return "Dockerfile Review";

      case "kubernetes":
        return "Kubernetes Review";

      case "terraform":
        return "Terraform Review";

      case "log":
        return "Log Analysis";
    }
  };

  const handleAnalyze = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (!input.trim()) {
      setError("Please provide some input.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResponse("");

      let result = "";

      switch (operation) {
        case "chat": {
          const data = await chat(input);
          result = data.response;
          break;
        }

        case "dockerfile": {
          const data =
            await reviewDockerfile(input);
          result = data.review;
          break;
        }

        case "kubernetes": {
          const data =
            await reviewKubernetes(input);
          result = data.review;
          break;
        }

        case "terraform": {
          const data =
            await reviewTerraform(input);
          result = data.review;
          break;
        }

        case "log": {
          const data = await explainLog(input);
          result = data.explanation;
          break;
        }
      }

      setResponse(result);
    } catch (err) {
      console.error(err);

      setError(
        "AI request failed. Please check the backend and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">

      {/* Header */}

      <div className="mb-8">
        <h1 className="text-4xl font-bold">
          AI Assistant
        </h1>

        <p className="text-gray-600 mt-2">
          Analyze DevOps problems using AI.
        </p>
      </div>

      {/* AI Form */}

      <div className="bg-white rounded-lg shadow p-6">

        <form onSubmit={handleAnalyze}>

          {/* Project */}

          <label className="block font-semibold mb-2">
            Project
          </label>

          <select
            value={selectedProject}
            onChange={(e) =>
              setSelectedProject(e.target.value)
            }
            disabled={
              loadingProjects ||
              projects.length === 0
            }
            className="border w-full p-3 rounded mb-6"
          >
            {projects.length === 0 ? (
              <option value="">
                {loadingProjects
                  ? "Loading projects..."
                  : "No projects available"}
              </option>
            ) : (
              projects.map((project) => (
                <option
                  key={project.id}
                  value={project.id}
                >
                  {project.name}
                </option>
              ))
            )}
          </select>

          {/* Operation */}

          <label className="block font-semibold mb-2">
            Operation
          </label>

          <select
            value={operation}
            onChange={(e) => {
              setOperation(
                e.target.value as Operation
              );

              setInput("");
              setResponse("");
              setError("");
            }}
            className="border w-full p-3 rounded mb-6"
          >
            <option value="log">
              Explain Application Log
            </option>

            <option value="chat">
              General DevOps Chat
            </option>

            <option value="dockerfile">
              Review Dockerfile
            </option>

            <option value="kubernetes">
              Review Kubernetes Manifest
            </option>

            <option value="terraform">
              Review Terraform
            </option>
          </select>

          {/* Input */}

          <label className="block font-semibold mb-2">
            Input
          </label>

          <textarea
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            placeholder={getPlaceholder()}
            rows={12}
            className="border w-full p-3 rounded font-mono text-sm"
          />

          {/* Error */}

          {error && (
            <div className="text-red-500 mt-4">
              {error}
            </div>
          )}

          {/* Submit */}

          <button
            type="submit"
            disabled={loading}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded"
          >
            {loading
              ? "Analyzing..."
              : "Analyze"}
          </button>

        </form>

      </div>

      {/* Response */}

      {response && (
        <div className="bg-white rounded-lg shadow p-6 mt-8">

          <h2 className="text-2xl font-semibold mb-4">
            {getResponseTitle()}
          </h2>

          <pre className="whitespace-pre-wrap text-sm leading-6">
            {response}
          </pre>

        </div>
      )}

    </div>
  );
}
