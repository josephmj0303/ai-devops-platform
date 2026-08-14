import { useEffect, useState } from "react";

import {
  analyzeLogs,
  analyzeDockerfile,
  analyzeKubernetes,
  analyzeTerraform,
  getAnalysisHistory,
} from "../api/ai";

import type {
  AnalysisSeverity,
  AIAnalysisHistoryItem,
  AnalysisType,
  DockerAnalysisResponse,
  KubernetesAnalysisResponse,
  TerraformAnalysisResponse,
  LogAnalysisResponse,
} from "../types/ai";

type AnalysisResult =
  | LogAnalysisResponse
  | DockerAnalysisResponse
  | KubernetesAnalysisResponse
  | TerraformAnalysisResponse;

const analysisLabels: Record<AnalysisType, string> = {
  logs: "Application Logs",
  dockerfile: "Dockerfile",
  kubernetes: "Kubernetes Manifest",
  terraform: "Terraform",
};

const placeholders: Record<AnalysisType, string> = {
  logs: `Paste application logs here...

Example:
ERROR: connection refused
database postgres:5432 is not reachable`,

  dockerfile: `Paste your Dockerfile here...

Example:
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]`,

  kubernetes: `Paste your Kubernetes manifest here...

Example:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app`,

  terraform: `Paste your Terraform configuration here...

Example:
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app" {
  ... 
}`,
};

function severityClass(
  severity: AnalysisSeverity
): string {
  return `severity-${severity}`;
}

function AIAssistant() {
  const [analysisType, setAnalysisType] =
    useState<AnalysisType>("logs");

  const [input, setInput] = useState("");
  const [result, setResult] =
    useState<AnalysisResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState<
    AIAnalysisHistoryItem[]
  >([]);

  const [historyLoading, setHistoryLoading] = useState(true);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getAnalysisHistory();
        setHistory(data);
      } catch (err) {
        console.error("Failed to load AI analysis history:", err);
      } finally {
        setHistoryLoading(false);
      }
    };

    loadHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!input.trim()) {
      setError("Please provide input for analysis.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      let response: AnalysisResult;

      switch (analysisType) {
        case "logs":
          response = await analyzeLogs(input);
          break;

        case "dockerfile":
          response = await analyzeDockerfile(input);
          break;

        case "kubernetes":
          response = await analyzeKubernetes(input);
          break;

        case "terraform":
          response = await analyzeTerraform(input);
          break;
      }

      setResult(response);

      const updatedHistory = await getAnalysisHistory();
      setHistory(updatedHistory);

      setError(
        "AI analysis failed. Please check the backend service and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleTypeChange = (
    type: AnalysisType
  ) => {
    setAnalysisType(type);
    setInput("");
    setResult(null);
    setError("");
  };

  return (
    <div className="ai-page">
      <div className="ai-header">
        <div>
          <h1>AI DevOps Assistant</h1>
          <p>
            Analyze DevOps configurations, infrastructure,
            and application logs using AI.
          </p>
        </div>
      </div>

      <div className="ai-console">
        <div className="ai-controls">
          <label htmlFor="analysis-type">
            Analysis Type
          </label>

          <select
            id="analysis-type"
            value={analysisType}
            onChange={(event) =>
              handleTypeChange(
                event.target.value as AnalysisType
              )
            }
          >
            <option value="logs">
              Application Logs
            </option>

            <option value="dockerfile">
              Dockerfile
            </option>

            <option value="kubernetes">
              Kubernetes Manifest
            </option>

            <option value="terraform">
              Terraform
            </option>
          </select>
        </div>

        <div className="ai-input-section">
          <label htmlFor="ai-input">
            {analysisLabels[analysisType]}
          </label>

          <textarea
            id="ai-input"
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            placeholder={placeholders[analysisType]}
            rows={16}
          />
        </div>

        {error && (
          <div className="ai-error">
            {error}
          </div>
        )}

        <button
          className="ai-analyze-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze with AI"}
        </button>
      </div>

      {result && (
        <AnalysisResultCard result={result} />
      )}
      <div className="ai-history">
        <div className="ai-history-header">
          <h2>Analysis History</h2>
          <span>{history.length} analyses</span>
        </div>

        {historyLoading ? (
          <p className="ai-history-empty">
            Loading history...
          </p>
        ) : history.length === 0 ? (
          <p className="ai-history-empty">
            No analysis history yet.
          </p>
        ) : (
          <div className="ai-history-list">
            {history.map((item) => (
              <div
                className="ai-history-item"
                key={item.id}
              >
                <div className="ai-history-main">
                  <div className="ai-history-title">
                    {analysisLabels[item.analysis_type]}
                  </div>

                  <div className="ai-history-summary">
                    {item.result.summary}
                  </div>

                  <div className="ai-history-meta">
                    <span>{item.result.component}</span>
                    <span>•</span>
                    <span>
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <span
                  className={`severity-badge ${severityClass(
                    item.result.severity
                  )}`}
                >
                  {item.result.severity.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

interface AnalysisResultCardProps {
  result: AnalysisResult;
}

function AnalysisResultCard({
  result,
}: AnalysisResultCardProps) {
  const isLogResult =
    "likely_cause" in result &&
    "impact" in result;

  return (
    <div className="ai-result">
      <div className="ai-result-header">
        <div>
          <h2>AI Analysis</h2>
          <span className="ai-component">
            {result.component}
          </span>
        </div>

        <span
          className={`severity-badge ${severityClass(
            result.severity
          )}`}
        >
          {result.severity.toUpperCase()}
        </span>
      </div>

      <div className="ai-result-section">
        <h3>Summary</h3>
        <p>{result.summary}</p>
      </div>

      {isLogResult ? (
        <>
          <div className="ai-result-section">
            <h3>Likely Cause</h3>
            <p>{result.likely_cause}</p>
          </div>

          <div className="ai-result-section">
            <h3>Impact</h3>
            <p>{result.impact}</p>
          </div>
        </>
      ) : (
        <div className="ai-result-section">
          <h3>Findings</h3>

          <ul>
            {result.findings?.map(
              (finding, index) => (
                <li key={index}>
                  {finding}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      <div className="ai-result-section">
        <h3>Recommended Actions</h3>

        <ul className="recommendations">
          {result.recommended_actions.map(
            (action, index) => (
              <li key={index}>
                <span className="checkmark">
                  ✓
                </span>

                <span>{action}</span>
              </li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}

export default AIAssistant;
